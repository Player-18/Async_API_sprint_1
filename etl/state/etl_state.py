import logging

from etl.backoff import backoff
from etl.state.redis_state_storage import State


class StateETL:
    def __init__(self, state: State):
        self.state = state

    # @backoff(limit_of_retries=10)
    def get_last_state(self, table_name: str):
        # Get last modified datetime.
        state_modified = self.state.get_state(f"{table_name}")

        # Set date if state doesn't exist.
        if state_modified:
            logging.info("State received successfully. The ETL process continues.")
        else:
            state_modified = "1800-01-01"
            self.state.set_state(f"{table_name}", state_modified)
            logging.info(f"There is no state for {table_name} ETL process. State was successfully created. The ETL "
                         f"process begins.")

        return state_modified

    @backoff(limit_of_retries=10)
    def set_last_state(self, table_name: str, last_modified: str, result: tuple):
        self.state.set_state(f"{table_name}", last_modified)
        if not result[0]:
            logging.error(f"Documents were not uploaded to ES.")
        elif result[0] == 1:
            logging.info(f"{result[0]} document was added to ES. State was updated.")
        else:
            logging.info(f"{result[0]} documents were added to ES. State was updated.")

    @backoff(limit_of_retries=10)
    def reset_state(self):
        self.state.set_state('film_work', "1800-01-01")
        self.state.set_state('genre', "1800-01-01")
        self.state.set_state('person', "1800-01-01")
