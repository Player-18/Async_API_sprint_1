from dataclasses import dataclass, asdict, field
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Base(BaseModel):
    id: str


class Genre(Base):
    name: str


class PersonName(Base):
    full_name: str


class Person(PersonName):
    role: List[str] = []
    film_ids: List[str] = []


class Film(Base):
    title: str
    description: str = None
    creation_date: date = None
    imdb_rating: Optional[float] = None
    genres: List[Genre] = []
    actors: List[PersonName] = []
    directors: List[PersonName] = []
    writers: List[PersonName] = []
