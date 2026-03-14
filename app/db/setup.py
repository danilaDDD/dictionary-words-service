from pymongo import MongoClient

from app.db.db import create_sync_db_client


def setup_db(settings):
    client = create_sync_db_client(settings)

    db = client[settings.DB_NAME]
    words = db.words
    words.create_index("text", unique=True)

    client.close()