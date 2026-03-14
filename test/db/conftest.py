import pytest
import pytest_asyncio

from app.db.db import create_db_client
from test.testutils.utils import cleanup_db

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session):
    await cleanup_db(session)

@pytest.fixture(scope="function")
def db_client(settings):
    return create_db_client(settings)