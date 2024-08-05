from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
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
@cache(expire=60)
async def person_search(
        query: str = Query('', description="Search query for person name"),
        page_size: int = Query(50, description="Number of persons per page"),
        page_number: int = Query(1, description="Page number"),
        person_service: PersonService = Depends(person_service),
) -> list[PersonWithFilms]:
    found_persons = await person_service.person_search(
        query=query,
        page_size=page_size,
        page_number=page_number
    )

    if not found_persons:
        raise HTTPException(status_code=404, detail=f"Person not found.")

    return found_persons


@router.get(
    "/",
    response_model=list[PersonUUID],
    summary="List of all persons.",
)
@cache(expire=60)
async def person(
        page_size: int = Query(50, description="Number of persons per page"),
        page_number: int = Query(1, description="Page number"),
        person_service: PersonService = Depends(person_service)
) -> list[PersonUUID]:
    person_list = await person_service.person_list(
        page_size=page_size,
        page_number=page_number
    )

    if not person_list:
        raise HTTPException(status_code=404, detail=f"There is no persons.")

    return person_list


@router.get(
    "/{person_id}",
    response_model=PersonWithFilms,
    summary="Person detail with films and roles in those films.",
)
@cache(expire=60)
async def persons(
        person_id: str = Path(..., description="The ID of person to find films with this person."),
        page_size: int = Query(50, description="Number of persons per page"),
        page_number: int = Query(1, description="Page number"),
        person_service: PersonService = Depends(person_service)
) -> PersonUUID:
    person = await person_service.person_detail(
        person_id=person_id,
        page_size=page_size,
        page_number=page_number
    )

    if not person:
        raise HTTPException(status_code=404, detail=f"No person with ID: {person_id}")

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
        raise HTTPException(status_code=404, detail="No films found with this person")

    return films



