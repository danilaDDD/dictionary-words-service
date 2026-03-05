import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from app.db.session_manager import SessionManager
from test.testutils.utils import cleanup_db


@pytest.fixture(scope="module")
def session_manager(db_client_factory) -> SessionManager:
    return SessionManager(db_client_factory)

@pytest.fixture(scope='function')
def client(settings):
    return create_db_client(settings)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_manager):
    await cleanup_db(session_manager)