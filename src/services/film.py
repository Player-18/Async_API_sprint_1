from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import FilmDetail


class FilmService:
    """Сервис фильмов."""

    index = "films"

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_film_from_elastic(self, film_id: str) -> Optional[FilmDetail]:
        """Получение фильма из Elasticsearch."""
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
            return doc['_source']
        except NotFoundError:
            return None


def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
