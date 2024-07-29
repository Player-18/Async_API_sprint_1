import logging
from elasticsearch import Elasticsearch

from etl.backoff import backoff
from etl.extract import Extract
from etl.load import load_data_to_elastic_search
from etl.settings import BaseConfigs
from etl.transform import transform_data_for_elasticsearch
from indices import movie_index, genre_index, person_index

logging.getLogger().setLevel(logging.INFO)


class ETL:
    def __init__(self, configs: BaseConfigs, table_name: str, index_name: str, index: dict):
        self.database_params = configs.dsn
        self.elasticsearch_host = configs.es_url
        self.etl_state = configs.etl_state
        self.size_of_batch = configs.batch
        self.table_name = table_name
        self.index_name = index_name
        self.index = index

    # @backoff(limit_of_retries=10)
    def create_index_if_doesnt_exist(self) -> None:
        """
        Function heck index, if it doesn't exist - create.
        :return: None
        """
        client = Elasticsearch(hosts=self.elasticsearch_host)

        if not client.indices.exists(index=self.index_name):
            response = client.indices.create(index=self.index_name, **self.index)
            if response.get("acknowledged"):
                logging.info(f"Index {self.index_name} was created successfully.")
            else:
                logging.error("Error of creating index.")

    def run_etl(self):

        # Check index, if it doesn't exist - create.
        self.create_index_if_doesnt_exist()

        extractor = Extract(self.table_name, self.database_params, self.size_of_batch)

        # Set initially value of size_of_current_batch as size_of_batch to begin cycle.
        size_of_current_batch = self.size_of_batch

        # Check size of batch from DB, if it will be not equals size_of_batch - finish cycle.
        while size_of_current_batch == self.size_of_batch:
            state_modified = self.etl_state.get_last_state(self.table_name)

            # Get batch of data with modified time starting from last_modified, with size of batch equals size_of_batch.
            # If size_of_current_batch not equals to size_of_batch - finish cycle.
            data_from_db, size_of_current_batch, last_modified = extractor.extract_data_from_db(state_modified)

            transformed_for_elasticsearch_data_from_db = transform_data_for_elasticsearch(index_name=self.index_name,
                                                                                          data_from_db=data_from_db)
            result_of_etl_loading = load_data_to_elastic_search(self.elasticsearch_host,
                                                                transformed_for_elasticsearch_data_from_db)

            # Set new state.
            self.etl_state.set_last_state(self.table_name, last_modified, result_of_etl_loading)


if __name__ == "__main__":
    configs = BaseConfigs()

    etl_movies = ETL(configs, table_name="film_work", index_name="movies", index=movie_index)
    etl_genres = ETL(configs, table_name="genre", index_name="genres", index=genre_index)
    etl_persons = ETL(configs, table_name="person", index_name="persons", index=person_index)

    etl_movies.run_etl()
    etl_genres.run_etl()
    etl_persons.run_etl()
    # configs.etl_state.reset_state()
