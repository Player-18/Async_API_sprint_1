from fastapi import APIRouter, Depends
from models.genre import Genre
from service.genres import GenreService, genre_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[Genre],
    summary="Список жанров",
)
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
async def genres(
    genre_id: str,
    genre_service: GenreService = Depends(genre_service),
) -> Genre:
    genre = await genre_service.genre_detail(
        genre_id
    )
    return genre
