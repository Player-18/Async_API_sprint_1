from typing import Optional, List

from pydantic import BaseModel, Field

from models.genre import GenreUUID
from models.person import PersonUUID


class FilmDetail(BaseModel):
    """Detailed model for a film, including its title, IMDb rating, description, and related entities."""

    uuid: str
    title: str
    imdb_rating: float
    description: str
    genres: List[GenreUUID]
    actors: List[PersonUUID]
    writers: List[PersonUUID]
    directors: List[PersonUUID]


class FilmIMBDSortedInput(BaseModel):
    """Model for film data sorted by IMDb rating, used for input purposes."""

    uuid: str = Field(alias="id")
    title: Optional[str]
    imdb_rating: Optional[float]


class FilmIMBDSortedOutput(BaseModel):
    """Model for film data sorted by IMDb rating, used for output purposes."""

    uuid: str
    title: Optional[str]
    imdb_rating: Optional[float]


