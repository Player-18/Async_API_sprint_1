from pydantic import BaseModel


class Person(BaseModel):
    """Модель персоны."""

    id: str
    full_name: str


class PersonUUID(BaseModel):
    """Модель персоны c UUID."""

    uuid: str
    full_name: str
