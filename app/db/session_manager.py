from typing import Generator

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from starlette.requests import Request

from app.db.db import DBClientFactory, get_db, get_db_client, create_db_client
from app.repositories.word_repository import WordRepository
from settings.settings import Settings, get_settings

class SessionManager:
    db: AsyncDatabase = None
    db_client_factory: DBClientFactory = None

    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def words(self) -> WordRepository:
        return WordRepository(self.db.words)

    def get_db(self) -> AsyncDatabase:
        return get_db(self.settings, self.client)

    def start(self) -> "SessionManager":
        self.client = create_db_client(self.settings)
        self.db = get_db(self.settings, self.client)
        return self

    async def close(self):
        await self.client.close()

def get_session_manager(request: Request) -> SessionManager:
    return request.app.state.session