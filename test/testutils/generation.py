from app.models.models import Word, Collection


def gen_word_object(text: str) -> Word:
    collection = Collection(name=text, id="collection")
    return Word(text="test", user_id=1, collections=[collection], translations=["translation"])