import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from etl.backoff import backoff
from etl.indices import filmwork_index


@backoff(limit_of_retries=10)
def create_index_if_doesnt_exist(index_name: str, index_body: dict, elasticsearch_host: str) -> None:
    """
    Function heck index, if it doesn't exist - create.
    :return: None
    """
    client = Elasticsearch(hosts=elasticsearch_host)

    if not client.indices.exists(index=index_name):
        response = client.indices.create(index=index_name, **index_body)
        if response.get("acknowledged"):
            logging.info(f"Index {index_name} was created successfully.")
        else:
            logging.error("Error of creating index.")


@backoff(limit_of_retries=10)
def load_data_to_elastic_search(elasticsearch_host: str, data: list):
    """
    Function for loading data to Elasticsearch.
    :param elasticsearch_host: Hosts of elasticsearch.
    :param data: List with prepared data for inserting to the Elasticsearch
    :return: Result of loading to ES.
    """
    client = Elasticsearch(hosts=elasticsearch_host)
    result = bulk(client, data)
    return result

