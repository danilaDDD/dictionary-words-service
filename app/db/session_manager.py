from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Callable

from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.db.client_factory import get_db_client_factory, DBClientFactory, get_db
from app.repositories.word_repository import WordRepository
from settings.settings import load_settings, Settings


class SessionManager:
    client: AsyncMongoClient = None
    db: AsyncDatabase = None
    db_client_factory: DBClientFactory = None

    def __init__(self, settings: Settings, db_client_factory: DBClientFactory):
        self.db_client_factory = db_client_factory
        self.settings = settings

    @property
    def words(self) -> WordRepository:
        return WordRepository(self.db.words)

    @asynccontextmanager
    async def start(self):
        try:
            self.client = self.db_client_factory()
            self.db = get_db(self.settings, self.client)
            yield self
        finally:
            await self.client.close()
            self.client = None


def get_session_manager(db_client_factory: DBClientFactory = Depends(get_db_client_factory),
                        settings: Settings = Depends(load_settings)) -> SessionManager:
    return SessionManager(settings, db_client_factory)