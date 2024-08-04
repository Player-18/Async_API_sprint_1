from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from db.elastic import get_elastic
from models.genre import Genre


class GenreService:
    """Сервис жанров."""

    index = "genres"

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def genre_detail(self, id: str) -> Genre | None:
        """Деталка жанра"""

        response = await self.elastic.get(
            index=self.index, id=id
        )

        if not response["_source"]:
            return None

        genre = Genre(**response["_source"])

        return genre

    async def genre_list(self, page_number: int, page_size: int) -> list[Genre] | None:
        """Получение списка жанров."""

        query = {
            "size": page_size,
            "query": {"match_all": {}},
            "from": (page_number - 1) * page_size,
        }

        response = await self.elastic.search(body=query, index=self.index)

        hits = response.get("hits")
        if not hits:
            return None

        genres = [Genre(**item["_source"]) for item in hits.get("hits")]
        return genres


def genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """Прослайка для внедрения зависимости сервиса жанров."""

    return GenreService(elastic)

