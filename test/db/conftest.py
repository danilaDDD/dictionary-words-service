import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from db.connection import create_session_factory


@pytest.fixture(scope="module")
def session_factory(settings) -> AsyncMongoClient:
    return create_session_factory(settings)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_factory):
    yield