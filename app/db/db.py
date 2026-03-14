from typing import Callable, Any

from fastapi.params import Depends
from pymongo import AsyncMongoClient, MongoClient
from starlette.requests import Request

from settings.settings import Settings, load_settings, get_settings

DBClientFactory = Callable[[], AsyncMongoClient]

def create_db_client(settings: Settings) -> AsyncMongoClient:
    return AsyncMongoClient(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        authSource=settings.AUTH_DB_NAME,
        authMechanism=settings.AUTH_ALGORITHM,
    )

def create_sync_db_client(settings: Settings) -> MongoClient:
    return MongoClient(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        authSource=settings.AUTH_DB_NAME,
        authMechanism=settings.AUTH_ALGORITHM,
)

def get_db_client(request: Request) -> AsyncMongoClient:
    return request.app.db_client


def get_db(settings: Settings, client: AsyncMongoClient | MongoClient) -> Any:
    db = client[settings.DB_NAME]
    return db
