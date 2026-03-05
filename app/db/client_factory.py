from typing import Callable, Any, Annotated

from fastapi.params import Depends
from pymongo import AsyncMongoClient, MongoClient

from settings.settings import Settings, load_settings


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

def get_db_client_factory(settings: Settings = Depends(load_settings)) -> DBClientFactory:
    return lambda: create_db_client(settings)

def get_db(settings: Settings, client: AsyncMongoClient | MongoClient) -> Any:
    client = create_db_client(settings)
    db = client[settings.DB_NAME]
    return db
