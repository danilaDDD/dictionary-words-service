import pytest
from bson import ObjectId
from starlette.responses import Response

from app.models.models import Collection
from test.testutils.asserts import assert_error_response
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.e2e
class TestUpdateWordRequest:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, session_manager, url_manager):
        self.api_client = api_client
        self.session_manager = session_manager
        self.url_manager = url_manager
        self.user_id = 3
        self.same_request_body = {'collections': [{'id': 'onertqwtrq', 'name': 'collection1',}]}
        yield

    @pytest.mark.parametrize(
        'updated_request_body',
        [
            {'collections': [{'id': 'onertqwtrq', 'name': 'collection1',}]},
            {'translations': ['text1', 'text2']},
            {'collections': [{'id': 'onertqwtrq', 'name': 'collection1',}], 'translations': ['text1', 'text2']},
        ]
    )
    async def test_with_valid_data_should_return_200_and_updated_word(self, updated_request_body: dict):
        word = gen_word_object(text='text', user_id=self.user_id)
        async with self.session_manager.start() as session:
            word_id_obj = await session.words.create(word)
            word_id = str(word_id_obj)

            resp = self.do_request(word_id, updated_request_body)

            assert resp.status_code == 200
            resp_json = resp.json()

            assert resp_json['id'] == word_id
            for field in updated_request_body:
                assert field in resp_json
                assert resp_json[field] == updated_request_body[field]
            assert resp_json['updated_at'] is not None
            assert resp_json['created_at'] is not None
            assert resp_json['updated_at'] != resp_json['created_at']

            words = await session.words.find_all()
            assert len(words) == 1
            updated_word = words[0]
            assert updated_word is not None
            assert updated_word.id == word_id
            if 'collections' in updated_request_body:
                assert len(updated_word.collections) == len(updated_request_body['collections'])
                for collection, collection_dict in zip(updated_word.collections, updated_request_body['collections']):
                    assert Collection.model_validate(collection_dict) == collection

            if 'translations' in updated_request_body:
                assert updated_word.translations == updated_request_body['translations']

    @pytest.mark.parametrize('invalid_data', [
        {},
        {'invalid_field': 'value'},
        {'collections': 'not_a_list'},
        {'translations': 'not_a_list'}
    ])
    async def test_with_invalid_request_should_return_400(self, invalid_data: dict):
        word = gen_word_object(text='text', user_id=self.user_id)
        async with self.session_manager.start() as session:
            word_id_obj = await session.words.create(word)
            word_id = str(word_id_obj)

            resp = self.do_request(word_id, invalid_data)

            assert_error_response(resp, 400)

            assert len(await session.words.find_all()) == 1

    async def test_with_nonexistent_word_id_should_return_404(self):
        non_existent_word_id = ObjectId()

        resp = self.do_request(str(non_existent_word_id), self.same_request_body)

        assert resp.status_code == 404

    async def test_with_unauthorized_user_should_return_403(self):
        word = gen_word_object(text='text', user_id=self.user_id)
        async with self.session_manager.start() as session:
            word_id_obj = await session.words.create(word)
            word_id = str(word_id_obj)

        other_user_id = self.user_id + 1
        resp = self.do_request(word_id, self.same_request_body, user_id=other_user_id)
        assert_error_response(resp, 403)

    def do_request(self, word_id: str, updated_request_body: dict, user_id: int = None) -> Response:
        user_id = self.user_id if user_id is None else user_id
        url = self.url_manager.get_word_by_id_url(user_id, word_id)
        return self.api_client.put(url, json=updated_request_body)

