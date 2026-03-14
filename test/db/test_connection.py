import pytest

from app.db.db import get_db


@pytest.mark.asyncio
async def test_connection(session) -> None:
    db = session.get_db()
    assert db is not None

    words = db.words
    assert words is not None
