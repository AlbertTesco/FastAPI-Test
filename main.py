import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db.database import create_tables, delete_tables
from api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function is used to manage the lifespan of the FastAPI application.
    It will clean up the database and create new tables when the application starts and stops.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    """
    await delete_tables()
    print("Database is cleaned up")
    await create_tables()
    print("Database is created")
    yield


app = FastAPI(lifespan=lifespan, docs_url='/')
app.include_router(router)
os.makedirs("media/images", exist_ok=True)
app.mount("/media/images", StaticFiles(directory="media/images"), name="media")
