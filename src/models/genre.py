from pydantic import BaseModel


class Genre(BaseModel):
    """Модель жанра."""

    id: str
    name: str
