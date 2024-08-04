from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from models.film import ListFilm
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


@router.get(
    "/{person_id}/film",
    response_model=List[ListFilm],
    summary="Films with person.",
)
@cache(expire=60)
async def films_with_person(
        person_id: str,
        person_service: PersonService = Depends(person_service),
) -> list[ListFilm] | None:
    films = await person_service.person_films(
        person_id
    )
    return films
