from pymongo import MongoClient

from app.db.client_factory import create_db_client

def setup_db(settings):
    client = MongoClient(settings.get_database_url())
    db = client.get_database()
    db.words.create_index("text", unique=True)
    client.close()