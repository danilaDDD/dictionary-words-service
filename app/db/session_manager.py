from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Callable

from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.db.client_factory import get_db_client_factory, DBClientFactory
from app.repositories.word_repository import WordRepository


class SessionManager:
    client: AsyncMongoClient = None
    db: AsyncDatabase = None
    db_client_factory: DBClientFactory = None

    def __init__(self, db_client_factory: DBClientFactory):
        self.db_client_factory = db_client_factory

    @property
    def words(self) -> WordRepository:
        return WordRepository(self.db.words)

    @asynccontextmanager
    async def start(self):
        try:
            self.client = self.db_client_factory()
            self.db = self.client.get_database()
            yield self
        finally:
            await self.client.close()
            self.client = None


def get_session_manager(db_client_factory: DBClientFactory = Depends(get_db_client_factory)) -> SessionManager:
    return SessionManager(db_client_factory)