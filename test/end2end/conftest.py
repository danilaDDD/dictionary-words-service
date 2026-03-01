import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient
from starlette.testclient import TestClient

from app.db.session_manager import SessionManager
from app.main import app
from test.testutils.utils import cleanup_db


@pytest.fixture(scope="module")
def session_manager(db_client_factory) -> SessionManager:
    return SessionManager(db_client_factory)

@pytest.fixture(scope="module")
def api_client():
    return TestClient(app)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_manager):
    await cleanup_db(session_manager)