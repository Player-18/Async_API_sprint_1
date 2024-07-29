import logging

import psycopg
from psycopg.rows import dict_row
from psycopg import ClientCursor

from etl.backoff import backoff


class Extract:
    def __init__(self, table_name: str, database_params, size_of_batch):
        self.table_name = table_name
        self.database_params = database_params
        self.size_of_batch = size_of_batch

    @backoff(limit_of_retries=10)
    def extract_data_from_db(self, state_modified: str) -> (list, int, str):
        """
        Function extract data from postgres DB.
        :param state_modified: Last modified data.
        :return: List of data, size of current batch, last modified data of filmwork.
        """
        with psycopg.connect(**self.database_params, row_factory=dict_row,
                             cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
            executed_data = {}

            if self.table_name == "film_work":
                # Get filmworks ids.
                cursor.execute(f"""SELECT table_name.id
                            FROM {self.table_name} table_name
                            WHERE table_name.modified > '{state_modified}'
                            ORDER BY table_name.modified
                            LIMIT {self.size_of_batch};
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
                executed_data = cursor.fetchall()

            elif self.table_name == "person":
                cursor.execute(f"""SELECT table_name.id, table_name.full_name, table_name.modified
                                            FROM {self.table_name} table_name
                                            WHERE table_name.modified > '{state_modified}'
                                            ORDER BY table_name.modified
                                            LIMIT {self.size_of_batch};
                                            """)
                executed_data = cursor.fetchall()
                size_of_current_batch = len(executed_data)

            elif self.table_name == "genre":
                cursor.execute(f"""SELECT table_name.id, table_name.name, table_name.description, table_name.modified
                                                            FROM {self.table_name} table_name
                                                            WHERE table_name.modified > '{state_modified}'
                                                            ORDER BY table_name.modified
                                                            LIMIT {self.size_of_batch};
                                                            """)
                executed_data = cursor.fetchall()
                size_of_current_batch = len(executed_data)

            # Get modified date of the last entry in the batch.
            last_modified = str(executed_data[-1]["modified"])

            return executed_data, size_of_current_batch, last_modified
