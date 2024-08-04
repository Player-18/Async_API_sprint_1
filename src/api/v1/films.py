from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from models.film import FilmDetail, FilmIMBDSortedInput, FilmIMBDSortedOutput
from models.genre import GenreUUID
from models.person import PersonUUID
from services.film import FilmService, get_film_service
from typing import List

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetail)
@cache(expire=60)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_film_from_elastic(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetail(
        uuid=film.get('id'),
        title=film.get('title'),
        imdb_rating=film.get('imdb_rating'),
        description=film.get('description'),
        genres=[
            GenreUUID(uuid=genre.get('id'),
                      name=genre.get('name')) for genre in film.get('genres')
        ],
        actors=[
            PersonUUID(uuid=actor.get('id'),
                       full_name=actor.get('name')) for actor in film.get('actors')
        ],
        writers=[
            PersonUUID(uuid=writer.get('id'),
                       full_name=writer.get('name')) for writer in film.get('writers')
        ],
        directors=[
            PersonUUID(uuid=director.get('id'),
                       full_name=director.get('name')) for director in film.get('directors')
        ]
    )


@router.get('/', response_model=List[FilmIMBDSortedOutput])
@cache(expire=60)
async def list_films_imbd_sorted(
        sort: str = Query("-", description="Sort order ('+' for ascending, '-' for descending)"),
        page_size: int = Query(50, le=100, description="Number of films per page"),
        page_number: int = Query(1, ge=1, description="Page number"),
        film_service: FilmService = Depends(get_film_service)
) -> List[FilmIMBDSortedInput]:

    films = await film_service.get_films_list_sorted(sort=sort, page_size=page_size, page_number=page_number)
    print('!!!asdasdas', films)

    if not films:
        raise HTTPException(status_code=404, detail="No films found")

    return [FilmIMBDSortedOutput(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]
