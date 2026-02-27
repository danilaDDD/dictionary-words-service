import os
from typing import Callable

import pytest
from pymongo import AsyncMongoClient

from settings.settings import load_settings, Settings


@pytest.fixture(scope="session", autouse=True)
def setup_all():
    os.environ['ENV'] = 'test'
    yield 


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()

@pytest.fixture(scope="session")
def db_client_factory(settings: Settings) -> Callable[[], AsyncMongoClient]:
    return lambda : AsyncMongoClient(settings.get_database_url())