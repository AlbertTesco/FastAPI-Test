from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.book import BookORM

DATABASE_URL = "sqlite+aiosqlite:///./books.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False})
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BookORM.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BookORM.metadata.drop_all)
