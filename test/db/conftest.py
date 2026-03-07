import pytest
import pytest_asyncio

from app.db.client_factory import create_db_client
from app.db.session_manager import SessionManager
from settings.settings import Settings
from test.testutils.utils import cleanup_db


@pytest.fixture(scope="module")
def session_manager(settings: Settings, db_client_factory) -> SessionManager:
    return SessionManager(settings, db_client_factory)

@pytest.fixture(scope='function')
def client(settings):
    return create_db_client(settings)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_manager):
    await cleanup_db(session_manager)