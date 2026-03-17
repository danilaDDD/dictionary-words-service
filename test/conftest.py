import asyncio
import os
from typing import Callable, Generator, AsyncGenerator, Any

import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from app.db.db import create_db_client
from app.db.session_manager import SessionManager
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

@pytest_asyncio.fixture(scope="function")
async def session(settings) -> AsyncGenerator[SessionManager, Any]:
    session_manager = SessionManager(settings)
    yield session_manager.start()
    await session_manager.close()

