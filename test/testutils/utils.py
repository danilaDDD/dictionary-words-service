from pymongo import AsyncMongoClient

from app.db.client_factory import get_db
from app.db.session_manager import SessionManager
from app.models.models import Word

class UrlManager:
    def get_words_url(self, user_id: int) -> str:
        return '/users/%d/words' % user_id

    def get_word_by_id_url(self, user_id: int, word_id: str) -> str:
        return '/users/%d/words/%s' % (user_id, word_id)


async def cleanup_db(session_manager: SessionManager):
    async with session_manager.start() as session:
        db = session.get_db()
        await db.words.delete_many({})
