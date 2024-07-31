from typing import Optional, List

from pydantic import BaseModel


class Film(BaseModel):
    """Модель фильма."""

    id: str
    imdb_rating: Optional[float]
    title: Optional[str]
    genres: Optional[List[str]]
    description: Optional[str]
    directors: Optional[List[dict]]
    actors: Optional[List[dict]]
    writers: Optional[List[dict]]
    directors_names: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]


class ListFilm(BaseModel):
    """Модель списка фильмов."""

    id: str
    imdb_rating: Optional[float]
    title: Optional[str]
