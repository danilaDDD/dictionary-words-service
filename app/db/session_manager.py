from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.repositories.word_repository import WordRepository
from settings.settings import Settings


class SessionManager:
    client: AsyncMongoClient = None
    db: AsyncDatabase = None

    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def words(self) -> WordRepository:
        return WordRepository(self.db.words)

    @asynccontextmanager
    async def start(self):
        try:
            self.client = AsyncMongoClient(self.settings.get_database_url())
            self.db = self.client.get_database()
            yield self
        finally:
            await self.client.close()
            self.client = None


def get_session_manager(settings: Settings) -> SessionManager:
    return SessionManager(settings)