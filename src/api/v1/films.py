from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from models.film import FilmDetail
from models.genre import GenreUUID
from models.person import PersonUUID
from services.film import FilmService, get_film_service

router = APIRouter()


@cache(expire=60)
@router.get('/{film_id}', response_model=FilmDetail)
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
