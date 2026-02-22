import pytest
from pymongo import AsyncMongoClient

from settings.settings import Settings

@pytest.mark.asyncio
async def test_connection(session_factory: AsyncMongoClient, settings: Settings) -> None:
    async with session_factory as client:
        db = client.get_database(settings.DB_NAME)
        assert db is not None