from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from models.film import FilmListOutput
from models.person import PersonUUID, PersonWithFilms
from services.persons import PersonService, person_service

router = APIRouter()


@router.get(
    "/search",
    response_model=List[PersonWithFilms],
    summary="Search for person, return person detail with films and roles in those films.",
)
# @cache(expire=60)
async def person_search(
        query: Optional[str] = Query('', description="Search query for person name"),
        page_number: int = 1,
        page_size: int = 50,
        person_service: PersonService = Depends(person_service),
) -> list[PersonWithFilms]:
    person = await person_service.person_search(
        query=query,
        page_size=page_size,
        page_number=page_number
    )
    return person


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
        page_number: int = 1,
        page_size: int = 50,
        person_service: PersonService = Depends(person_service),
) -> PersonUUID:
    person = await person_service.person_detail(
        person_id=person_id,
        page_size=page_size,
        page_number=page_number
    )
    return person


@router.get(
    "/{person_id}/film",
    response_model=List[FilmListOutput],
    summary="Films with person.",
)
@cache(expire=60)
async def films_with_person(
        person_id: str,
        page_number: int = 1,
        page_size: int = 50,
        person_service: PersonService = Depends(person_service),
) -> list[FilmListOutput] | None:
    films = await person_service.person_films(
        person_id=person_id,
        page_number=page_number,
        page_size=page_size
    )
    if not films:
        raise HTTPException(status_code=404, detail="No films found for this person")

    return films



