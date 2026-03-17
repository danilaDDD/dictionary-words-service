import pytest
from starlette.responses import Response

from test.testutils.asserts import assert_error_response, assert_dict_with_word_object
from test.testutils.generation import gen_create_word_request_body


@pytest.mark.asyncio
@pytest.mark.e2e
class TestCreateWordRequest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session, api_client, url_manager):
        self.session = session
        self.api_client = api_client
        self.url_manager = url_manager
        self.user_id = 1
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


        words = await self.session.words.find_all()
        assert len(words) == 1

        word = words[0]
        assert word.id is not None
        assert_dict_with_word_object(word_request, word)

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

        words = await self.session.words.find_all()
        assert len(words) == 1

    def do_request(self, word_request: dict) -> Response:
        return self.api_client.post(self.url_manager.get_words_url(self.user_id),
                                    json=word_request)