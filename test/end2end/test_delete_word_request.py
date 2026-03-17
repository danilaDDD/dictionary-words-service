import pytest

from test.testutils.asserts import assert_error_response
from test.testutils.generation import gen_word_object


@pytest.mark.e2e
@pytest.mark.asyncio
class TestDeleteWordRequest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session, api_client, url_manager):
        self.session = session
        self.api_client = api_client
        self.url_manager = url_manager
        self.user_id = 1
        yield

    async def test_with_valid_word_id_should_return_200_and_delete_word(self):
        word = gen_word_object(text='text', user_id=self.user_id)
        word_id = await self.session.words.create(word)

        resp = self.do_request(str(word_id))
        assert resp.status_code == 200
        assert resp.json() != {}

        words = await self.session.words.find_all()
        assert len(words) == 0

    async def test_with_non_existent_word_id_should_return_404(self):
        non_existent_word_id = "uyfeyufey"

        resp = self.do_request(non_existent_word_id)
        assert_error_response(resp, 404)

    async def test_with_invalid_word_id_should_return_404(self):
        invalid_word_id = "invalid_id"

        resp = self.do_request(invalid_word_id)
        assert_error_response(resp, 404)

    async def test_with_invalid_user_id_should_return_403(self):
        word = gen_word_object(text='text', user_id=self.user_id)

        word_id = await self.session.words.create(word)

        resp = self.do_request(word_id, user_id=999)
        assert_error_response(resp, 403)

    def do_request(self, word_id: str, user_id: int = None):
        url = self.url_manager.get_word_by_id_url(user_id or self.user_id, word_id)
        return self.api_client.delete(url)