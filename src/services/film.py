from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import FilmDetail, FilmIMBDSortedInput


class FilmService:
    """Сервис фильмов."""

    index = "movies"

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_film_from_elastic(self, film_id: str) -> Optional[FilmDetail]:
        """Получение фильма из Elasticsearch."""
        try:
            doc = await self.elastic.get(index=self.index, id=film_id)
            return doc['_source']
        except NotFoundError:
            return None

    async def get_films_list_sorted(self,
                                    sort: str,
                                    page_number: int,
                                    page_size: int,
                                    genre_id: Optional[str] = None
                                    ) -> list[FilmIMBDSortedInput] | None:
        """Получение списка фильмов отсортированных по рейтингу IMBD."""

        sort_dict = {"+": "asc", "-": "desc"}

        filter_conditions = []
        if genre_id:
            # Handle nested field filtering for genre_id
            filter_conditions.append({
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"genres.id": genre_id}}
                            ]
                        }
                    }
                }
            })

        # Build the query
        query = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": [{"match_all": {}}],
                    "filter": filter_conditions
                }
            },
            "sort": [{sort[1:]: {"order": sort_dict.get(sort[0])}}],
            "from": (page_number - 1) * page_size,
        }

        response = await self.elastic.search(body=query, index=self.index)

        hits = response.get("hits")
        if not hits:
            return None

        films = [FilmIMBDSortedInput(**item["_source"]) for item in hits.get("hits")]
        return films


def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
