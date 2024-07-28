import logging
import sys

from etl.extract import extract_data_from_db
from etl.load import load_data_to_elastic_search, create_index_if_doesnt_exist
from etl.settings import BaseConfigs
from etl.transform import transform_data_for_elasticsearch
from indices import filmwork_index, genre_index, person_index
logging.getLogger().setLevel(logging.INFO)


class ETL:

    def __init__(self, configs: BaseConfigs):
        self.database_params = configs.dsn
        self.elasticsearch_host = configs.es_url
        self.etl_state = configs.etl_state
        self.size_of_batch = configs.batch

    def create_indices(self):
        create_index_if_doesnt_exist("movies", filmwork_index, self.elasticsearch_host)
        create_index_if_doesnt_exist("genres", genre_index, self.elasticsearch_host)
        create_index_if_doesnt_exist("persons", person_index, self.elasticsearch_host)

    def run_etl(self):
        # Set initially value of size_of_current_batch as size_of_batch to begin cycle.
        size_of_current_batch = self.size_of_batch

        # Check size of batch from DB, if it will be not equals size_of_batch - finish cycle.
        while size_of_current_batch == self.size_of_batch:

            state_modified = self.etl_state.get_last_state()

            # Get data with modified time starting from last_modified, with size of batch equals size_of_batch.
            data_from_db, size_of_current_batch, last_modified = extract_data_from_db(self.database_params,
                                                                                      state_modified,
                                                                                      self.size_of_batch)

            transformed_for_elasticsearch_data_from_db = transform_data_for_elasticsearch(data_from_db)

            result_of_etl_loading = load_data_to_elastic_search(self.elasticsearch_host,
                                                                transformed_for_elasticsearch_data_from_db)

            # Set new state.
            self.etl_state.set_last_state(last_modified, result_of_etl_loading)


if __name__ == "__main__":
    configs = BaseConfigs()

    etl = ETL(configs)

    etl.create_indices()
    # etl.run_etl()
    # etl.etl_state.reset_state()