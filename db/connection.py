from fastapi import Depends
from pymongo import AsyncMongoClient

from settings.settings import Settings, load_settings


def create_session_factory(settings: Settings) -> AsyncMongoClient:
    return AsyncMongoClient(
        settings.get_database_url(),
    )



def get_session_factory(settings: Settings = Depends(load_settings, use_cache=True)) -> AsyncMongoClient:
    return create_session_factory(settings)