import logging

import psycopg
from psycopg.rows import dict_row
from psycopg import ClientCursor

from etl.backoff import backoff


@backoff(limit_of_retries=10)
def extract_data_from_db(db_params: dict, state_modified: str, size_of_batch: int) -> (list, int, str):
    """
    Function extract data from postgres DB.
    :param db_params: Parameters of DB connection.
    :param state_modified: Last modified data.
    :param size_of_batch: Size of batch.
    :return: List of data, size of current batch, last modified data of filmwork.
    """
    with psycopg.connect(**db_params, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
        # Get list of filmwork's id.
        cursor.execute(f"""SELECT fw.id
                        FROM film_work fw
                        WHERE fw.modified > '{state_modified}'
                        ORDER BY fw.modified
                        LIMIT {size_of_batch};
                        """)

        executed_data = cursor.fetchall()
        films_id_in_batch = [str(entry["id"]) for entry in executed_data]
        size_of_current_batch = len(films_id_in_batch)

        if size_of_current_batch == 0:
            logging.info('There is no new data to extract.')
            return [], 0, state_modified

        films_id_in_batch_string = "', '".join(films_id_in_batch)

        # Enrich filmworks with data.
        cursor.execute(f"""
            SELECT
                fw.id as fw_id, 
                fw.title, 
                fw.description, 
                fw.rating, 
                fw.type, 
                fw.created, 
                fw.modified, 
                pfw.role as person_role, 
                p.id as person_id, 
                p.full_name as person_full_name,
                g.name as genre_name
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id IN ('{films_id_in_batch_string}')
            ORDER BY fw.modified;
        """)

        films_batch_executed_data = cursor.fetchall()

        # Get modified date of the last filmwork in the batch.
        last_modified = str(films_batch_executed_data[-1]["modified"])

        return films_batch_executed_data, size_of_current_batch, last_modified
