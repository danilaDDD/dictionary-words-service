import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from app.db.session_manager import SessionManager

@pytest.fixture(scope="module")
def session_manager(settings) -> SessionManager:
    return SessionManager(settings)

@pytest.fixture(scope='function')
def client(settings):
    return AsyncMongoClient(settings.get_database_url())

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_manager):
    async with session_manager.start() as session:
        db = session.client.get_database()
        await db.words.delete_many({})