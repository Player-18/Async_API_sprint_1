from typing import Optional, List

from pydantic import BaseModel, Field

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


class FilmIMBDSortedInput(BaseModel):
    """Модель фильма отсортированного по рейтингу IMBD."""

    uuid: str = Field(alias="id")
    title: Optional[str]
    imdb_rating: Optional[float]


class FilmIMBDSortedOutput(BaseModel):
    """Модель фильма отсортированного по рейтингу IMBD."""

    uuid: str
    title: Optional[str]
    imdb_rating: Optional[float]


class ListFilm(BaseModel):
    """Модель списка фильмов."""

    id: str
    imdb_rating: Optional[float]
    title: Optional[str]
