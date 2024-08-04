from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from db.elastic import get_elastic
from models.person import PersonUUID


class PersonService:
    """Service of person."""

    index = "persons"

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def person_detail(self, id: str) -> PersonUUID | None:
        """Detail of person"""

        response = await self.elastic.get(
            index=self.index, id=id
        )

        if not response["_source"]:
            return None
        print(response)
        person = PersonUUID(uuid=response["_source"].get('id'), full_name=response["_source"].get('name'))

        return person

    async def person_list(self, page_number: int, page_size: int) -> list[PersonUUID] | None:
        """Get list of person"""

        query = {
            "size": page_size,
            "query": {"match_all": {}},
            "from": (page_number - 1) * page_size,
        }

        response = await self.elastic.search(body=query, index=self.index)

        hits = response.get("hits")
        if not hits:
            return None
        print(hits)
        persons = [PersonUUID(uuid=item["_source"].get('id'), full_name=item["_source"].get('name')) for item in hits.get(
            "hits")]
        return persons


def person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """Dependency for person service"""

    return PersonService(elastic)

