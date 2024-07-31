from pydantic import BaseModel


class Person(BaseModel):
    """Модель персоны."""

    id: str
    full_name: str
