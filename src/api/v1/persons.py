from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from models.person import PersonUUID, PersonWithFilms
from services.persons import PersonService, person_service

router = APIRouter()


@router.get(
    "/",
    response_model=list[PersonUUID],
    summary="List of persons",
)
@cache(expire=60)
async def person(
    person_service: PersonService = Depends(person_service),
    page: int = 1,
    page_size: int = 10
) -> list[PersonUUID]:
    person_list = await person_service.person_list(
        page, page_size
    )
    return person_list


@router.get(
    "/{person_id}",
    response_model=PersonWithFilms,
    summary="Person detail with films and roles in those films.",
)
@cache(expire=60)
async def persons(
    person_id: str,
    person_service: PersonService = Depends(person_service),
) -> PersonUUID:
    person = await person_service.person_detail(
        person_id
    )
    return person
