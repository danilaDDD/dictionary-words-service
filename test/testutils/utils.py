from app.db.session_manager import SessionManager


async def cleanup_db(session_manager: SessionManager):
    async with session_manager.start() as session:
        db = session.client.get_database()
        await db.words.delete_many({})