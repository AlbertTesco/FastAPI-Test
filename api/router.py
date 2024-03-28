import base64
import os
from typing import List

import aiofiles
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from logger_config import setup_logger
from models.book import BookORM
from shemas.book import SBookBase, SBookFilters

router = APIRouter()
logger = setup_logger()


@router.post("/add_books")
async def add_books(books: List[SBookBase], db: AsyncSession = Depends(get_db)):
    """
    This function adds a list of books to the database.

    Args:
        books (List[SBookBase]): The list of books to add.
        db (AsyncSession): The database session.

    Returns:
        Dict: A dictionary with a single key, "success", indicating whether the operation was successful.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    async with db.begin():
        for book_data in books:
            photo_base64 = book_data.photo

            try:
                photo_base64 = photo_base64.split(",")[-1]
                photo_content = base64.b64decode(photo_base64)
            except Exception as e:
                logger.error(f"Ошибка при декодировании изображения для книги {book_data.name}: {e}")
                continue

            new_book = BookORM(
                name=book_data.name,
                author=book_data.author,
                genre=book_data.genre,
                photo=None,
                price=book_data.price
            )

            db.add(new_book)
            await db.flush()

            book_id = new_book.id
            os.makedirs("media/images", exist_ok=True)
            filename = f"media/images/{book_id}-{book_data.name.replace(' ', '-')}-{book_data.author.replace(' ', '-')}.png"

            try:
                async with aiofiles.open(filename, 'wb') as f:
                    await f.write(photo_content)
            except Exception as e:
                logger.error(f"Ошибка при сохранении файла для книги {book_data.name}: {e}")

            new_book.photo = '/' + filename

    try:
        await db.commit()
    except sqlalchemy.exc.OperationalError as e:
        logger.error(f"Ошибка сети при коммите сессии: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сети при сохранении книги")
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(f"Ошибка целостности данных при коммите сессии: {e}")
        raise HTTPException(status_code=400, detail="Ошибка целостности данных при сохранении книги")
    except sqlalchemy.exc.ProgrammingError as e:
        logger.error(f"Ошибка синтаксиса SQL при коммите сессии: {e}")
        raise HTTPException(status_code=400, detail="Ошибка синтаксиса SQL при сохранении книги")
    except Exception as e:
        logger.error(f"Неизвестная ошибка при коммите сессии: {e}")
        raise HTTPException(status_code=500, detail="Неизвестная ошибка при сохранении книги")

    return {"success": True}


@router.get("/find_books", response_model=List[SBookBase])
async def find_books(filters: SBookFilters, db: AsyncSession = Depends(get_db)):
    """
    This function finds books in the database based on the provided filters.

    Args:
        filters (SBookFilters): The filters to use for searching.
        db (AsyncSession): The database session.

    Returns:
        List[SBookBase]: A list of books that match the provided filters.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    async with db.begin():
        stmt = select(BookORM)
        if filters.name:
            # Filter by name (case-insensitive)
            stmt = stmt.filter(BookORM.name.ilike(f"%{filters.name}%"))
        if filters.author:
            # Filter by author (case-insensitive)
            stmt = stmt.filter(BookORM.author.ilike(f"%{filters.author}%"))
        if filters.genre:
            # Filter by genre
            stmt = stmt.filter(BookORM.genre == filters.genre)
        if filters.price_from:
            # Filter by price (greater than or equal to)
            stmt = stmt.filter(BookORM.price >= filters.price_from)
        if filters.price_to:
            # Filter by price (less than or equal to)
            stmt = stmt.filter(BookORM.price <= filters.price_to)

        result = await db.execute(stmt)
        books_orm = result.scalars().all()

        # Convert the ORM objects to SBookBase objects
        books_base = [SBookBase.from_orm(book) for book in books_orm]

    return books_base
