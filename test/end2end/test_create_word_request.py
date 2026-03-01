import pytest
from starlette.responses import Response

from app.models.models import Collection
from test.testutils.asserts import assert_error_response
from test.testutils.generation import gen_create_word_request_body


@pytest.mark.asyncio
@pytest.mark.e2e
class TestCreateWordRequest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session_manager, api_client):
        self.session_manager = session_manager
        self.api_client = api_client
        self.url = "/words/"
        yield

    async def test_with_valid_data_should_return_201_and_created_word(self):
        word_request = gen_create_word_request_body("text")

        resp = self.do_request(word_request)
        assert resp.status_code == 201
        resp_json = resp.json()

        assert 'id' in resp_json
        for field in word_request:
            assert field in resp_json
            assert resp_json[field] == word_request[field]
        assert resp_json['created_at'] is not None
        assert resp_json['updated_at'] is not None

        async with self.session_manager.start() as session:
            words = await session.words.find_all()
            assert len(words) == 1

            word = words[0]
            assert word.id is not None
            assert word.text == word_request['text']

            for collection_dict, collection in zip(word_request['collections'], word.collections):
                assert Collection.model_validate(collection_dict) == collection

            assert word.translations == word_request['translations']
            assert word.created_at is not None
            assert word.updated_at is not None

    @pytest.mark.parametrize(
        'invalid_data',
        [
            {},
            {'text': 'text'},
            {'text': 'text', 'user_id': 1},
            {'text': 'text', 'user_id': 1, 'collections': []},
            {'text': 'text', 'user_id': 1, 'translations': []},
            {'text': 'text', 'collections': []},
            {'text': 'text', 'translations': []},
            {'user_id': 1, 'collections': [], 'translations': []},
            {'invalid_field': 'value'},
        ]
    )
    async def test_with_invalid_data_should_return_400(self, invalid_data):
        resp = self.do_request(invalid_data)
        assert_error_response(resp, 400)

    async def test_duplicate_request_should_return_400_and_not_create_word(self):
        word_request = gen_create_word_request_body("text")

        self.do_request(word_request)

        resp2 = self.do_request(word_request)
        assert_error_response(resp2, 400)

        async with self.session_manager.start() as session:
            words = await session.words.find_all()
            assert len(words) == 1

    def do_request(self, word_request: dict) -> Response:
        return self.api_client.post(self.url, json=word_request)