import pytest

from app.models.models import Collection, Word
from test.testutils.asserts import assert_error_response
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.e2e
class TestGetWordDetailsRequest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session_manager, api_client, url_manager):
        self.session_manager = session_manager
        self.api_client = api_client
        self.url_manager = url_manager
        self.user_id = 1
        yield

    async def test_with_valid_id_should_return_200_and_word_details(self):
        word = await self.create_word()

        resp = self.do_request(word.id)

        assert resp.status_code == 200
        resp_json = resp.json()

        assert resp_json['id'] == word.id
        assert resp_json['text'] == word.text
        assert resp_json['user_id'] == word.user_id
        parsed_collection = [Collection.model_validate(c) for c in resp_json['collections']]
        assert word.collections == parsed_collection
        assert resp_json['translations'] == word.translations

    async def test_with_invalid_user_id_should_return_403(self):
        word = await self.create_word()
        resp = self.do_request(word.id, user_id=999)
        assert_error_response(resp, 403)

    async def test_with_invalid_id_should_return_404(self):
        resp = self.do_request("nonexistent_id")
        assert_error_response(resp, 404)

    async def test_with_not_exist_id_should_return_404(self):
        resp = self.do_request("d73263t272372")
        assert_error_response(resp, 404)


    async def create_word(self) -> Word:
        word = gen_word_object("text", user_id=self.user_id)
        async with self.session_manager.start() as session:
            id_obj = await session.words.create(word)
            return await session.words.find_by_id(id_obj)

    def do_request(self, word_id: str, user_id: int = None):
        url = self.url_manager.get_word_by_id_url(user_id or self.user_id, word_id)
        return self.api_client.get(url)
