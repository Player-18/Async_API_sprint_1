from typing import Optional, List

from pydantic import BaseModel

from models.genre import GenreUUID
from models.person import PersonUUID


class FilmDetail(BaseModel):
    """Модель фильма."""

    uuid: str
    title: str
    imdb_rating: float
    description: str
    genres: List[GenreUUID]
    actors: List[PersonUUID]
    writers: List[PersonUUID]
    directors: List[PersonUUID]


class ListFilm(BaseModel):
    """Модель списка фильмов."""

    id: str
    imdb_rating: Optional[float]
    title: Optional[str]
