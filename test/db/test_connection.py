import pytest

from app.db.client_factory import get_db


@pytest.mark.asyncio
async def test_connection(client, settings) -> None:
    db = get_db(settings, client)
    assert db is not None

    words = db.words
    assert words is not None

    await client.close()
