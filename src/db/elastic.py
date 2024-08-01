from typing import Optional
from elasticsearch import AsyncElasticsearch

from core import config

es: Optional[AsyncElasticsearch] = None

# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return AsyncElasticsearch(hosts=[f'{config.ELASTIC_SCHEMA}{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
