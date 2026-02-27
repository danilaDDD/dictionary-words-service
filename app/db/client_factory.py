from typing import Callable, Any, Annotated

from fastapi.params import Depends
from pymongo import AsyncMongoClient

from settings.settings import Settings, load_settings


DBClientFactory = Callable[[], AsyncMongoClient]

def create_db_client(settings: Settings) -> AsyncMongoClient:
    return AsyncMongoClient(settings.get_database_url())

def get_db_client_factory(settings: Settings = Depends(load_settings)) -> DBClientFactory:
    return lambda: create_db_client(settings)
