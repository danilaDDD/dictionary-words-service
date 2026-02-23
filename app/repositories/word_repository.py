from pymongo import AsyncMongoClient

from app.models.models import Word
from app.repositories.base import BaseRepository


class WordRepository(BaseRepository):
    model = Word