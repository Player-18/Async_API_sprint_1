import logging

from etl.backoff import backoff
from etl.state.redis_state_storage import State


class StateETL:
    def __init__(self, state: State):
        self.state = state

    # @backoff(limit_of_retries=10)
    def get_last_state(self):
        # Get last modified datetime.
        state_modified = self.state.get_state("last_modified")

        # Set date if state doesn't exist.
        if state_modified:
            logging.info("State received successfully. The ETL process continues.")
        else:
            state_modified = "1800-01-01"
            self.state.set_state("last_modified", state_modified)
            logging.info("There is no state for ETL process. State was successfully created. The ETL process begins.")

        return state_modified

    @backoff(limit_of_retries=10)
    def set_last_state(self, last_modified: str, result: tuple):
        self.state.set_state('last_modified', last_modified)
        if not result[0]:
            logging.error(f"Documents were not uploaded to ES.")
        elif result[0] == 1:
            logging.info(f"{result[0]} document was added to ES. State was updated.")
        else:
            logging.info(f"{result[0]} documents were added to ES. State was updated.")

    @backoff(limit_of_retries=10)
    def reset_state(self):
        self.state.set_state('last_modified', "1800-01-01")
