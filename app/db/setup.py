from pymongo import MongoClient, ASCENDING

from app.db.db import create_sync_db_client


def setup_db(settings):
    client = create_sync_db_client(settings)

    db = client[settings.DB_NAME]
    words = db.words

    words.drop_indexes()
    words.create_index([("user_id", ASCENDING),
                        ("text", ASCENDING),], unique=True)
    words.create_index([("user_id", ASCENDING),])

    for index in words.list_indexes():
        print(index)

    client.close()