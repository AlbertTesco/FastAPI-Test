from pydantic import BaseModel
from typing import List, Optional

from models.book import Genre


class SBookBase(BaseModel):
    """
    Base model for books.

    Args:
        name (str): Name of the book.
        author (str): Name of the author.
        genre (Genre): Genre of the book.
        price (float): Price of the book.
        photo (str): Photo in base64.

    Attributes:
        id (int): Unique ID of the book.
        created_at (datetime): Date and time the book was created.
        updated_at (datetime): Date and time the book was last updated.
    """

    name: str
    author: str
    genre: Genre
    price: float
    photo: str

    class Config:
        orm_mode = True
        from_attributes = True


class SBookFilters(BaseModel):
    """
    This class is used to filter books based on various criteria.

    Attributes:
        name (Optional[str]): Filter books by name.
        author (Optional[str]): Filter books by author.
        genre (Optional[Genre]): Filter books by genre.
        price_from (Optional[float]): Filter books by price greater than or equal to this value.
        price_to (Optional[float]): Filter books by price less than or equal to this value.
    """

    name: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[Genre] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None
