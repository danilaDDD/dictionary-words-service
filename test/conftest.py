import os
from typing import Callable

import pytest
from pymongo import AsyncMongoClient

from app.db.client_factory import create_db_client
from settings.settings import load_settings, Settings
from test.testutils.utils import UrlManager


@pytest.fixture(scope="session", autouse=True)
def setup_all():
    os.environ['ENV'] = 'test'
    yield 


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()

@pytest.fixture(scope="session")
def url_manager() -> UrlManager:
    return UrlManager()

@pytest.fixture(scope="session")
def db_client_factory(settings: Settings) -> Callable[[], AsyncMongoClient]:
    return lambda : create_db_client(settings)