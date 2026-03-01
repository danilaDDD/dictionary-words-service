from app.db.setup import setup_db
from settings.settings import load_settings


def setup():
    settings = load_settings()
    setup_db(settings)

if __name__ == '__main__':
    setup()