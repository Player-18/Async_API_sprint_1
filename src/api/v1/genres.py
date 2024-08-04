from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from models.film import FilmIMBDSortedOutput
from models.genre import Genre
from service.genres import GenreService, genre_service

router = APIRouter()


@router.get(
    "/",
    response_model=list[Genre],
    summary="Список жанров",
)
@cache(expire=60)
async def genres(
        genre_service: GenreService = Depends(genre_service),
        page: int = 1,
        page_size: int = 10
) -> list[Genre]:
    genres_list = await genre_service.genre_list(
        page, page_size
    )
    return genres_list


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Деталка жанра",
)
@cache(expire=60)
async def genres(
        genre_id: str,
        genre_service: GenreService = Depends(genre_service),
) -> Genre:
    genre = await genre_service.genre_detail(
        genre_id
    )
    return genre


@router.get(
    "/{genre_id}/popular",
    response_model=List[FilmIMBDSortedOutput],
    summary="Get popular films by genre"
)
@cache(expire=60)
async def genres(
        genre_id: str,
        page_number: int = 1,
        page_size: int = 50,
        genre_service: GenreService = Depends(genre_service)
) -> List[FilmIMBDSortedOutput]:
    films = await genre_service.get_popular_films(
        genre_id=genre_id,
        page_number=page_number,
        page_size=page_size
    )

    if not films:
        raise HTTPException(status_code=404, detail="No films found for this genre")

    return [FilmIMBDSortedOutput(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]
