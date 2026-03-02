from app.models.models import Word, Collection
from app.schemas.requests import CreateWordRequest


def gen_word_object(text: str, user_id: int = None) -> Word:
    collection = Collection(name=text, id="collection")
    return Word(text="test",
                user_id=user_id if user_id is not None else 1,
                collections=[collection], translations=["translation"])

def gen_create_word_request_body(text: str) -> dict:
    return {
        "text": text,
        "user_id": 1,
        "collections": [
            {
                "id": "6et72737623",
                "name": "collection1"
            },
            {
                "id": "dg77du2u3u32",
                "name": "collection2"
            }
        ],
        "translations": ["translation", "translation2"]
    }
