from fastapi import Response

from app.models.models import Word, Collection


def assert_error_response(response: Response, status_code: int):
    json = response.json()
    assert response.status_code == status_code
    assert "detail" in json and len(json["detail"]) > 0

def assert_dict_with_word_object(word_request: dict, word: Word):
    assert word.text == word_request['text']

    for collection_dict, collection in zip(word_request['collections'], word.collections):
        assert Collection.model_validate(collection_dict) == collection

    assert word.translations == word_request['translations']
    assert word.created_at is not None
    assert word.updated_at is not None
