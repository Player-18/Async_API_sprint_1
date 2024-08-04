from pydantic import BaseModel


class Genre(BaseModel):
    """Модель жанра."""

    id: str
    name: str


class GenreUUID(BaseModel):
    """Модель жанра, принимающая поле UUID."""

    uuid: str
    name: str
