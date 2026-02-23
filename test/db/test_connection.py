import pytest
from pymongo import AsyncMongoClient

from settings.settings import Settings

@pytest.mark.asyncio
async def test_connection(client) -> None:
    db = client.get_database()
    assert db is not None

    words = db.words
    assert words is not None

    await client.close()
