import logging


def log_etl_result(result, table_name):
    if not result[0]:
        logging.info(f"Documents of '{table_name}' were not uploaded to ES.")
    elif result[0] == 1:
        logging.info(f"{result[0]} document was added to ES. State was updated.")
    else:
        logging.info(f"{result[0]} documents were added to ES. State was updated.")