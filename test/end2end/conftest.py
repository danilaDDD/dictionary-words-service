# Оберну создание TestClient в контекстный менеджер, чтобы lifespan FastAPI правильно стартовал и завершался
import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from app.main import app
from test.testutils.utils import cleanup_db


@pytest.fixture(scope="module")
def api_client():
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session):
    await cleanup_db(session)

