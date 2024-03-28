import enum

from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Genre(enum.Enum):
    """
    An enumeration.

    This class inherits from the built-in enum.Enum class and defines a set of named constants.
    The constants are unique and can be compared by identity, and they can be converted to and from strings.

    The members of the Genre enumeration are:

    - fantasy
    - detective
    - history
    - other

    """

    fantasy = "fantasy"
    detective = "detective"
    history = "history"
    other = "other"


class BookORM(Base):
    """
    The BookORM class represents a book in the database.

    Attributes:
        id (int): The unique identifier of the book.
        name (str): The name of the book.
        author (str): The name of the author.
        genre (Genre): The genre of the book.
        photo (str): The URL of the book's cover photo.
        price (float): The price of the book.

    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(Enum(Genre))
    photo = Column(String)
    price = Column(Float)
