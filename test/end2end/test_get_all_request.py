import pytest

from test.testutils.asserts import assert_dict_with_word_object
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.e2e
class TestGetAllWordRequest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session, api_client, url_manager):
        self.session = session
        self.api_client = api_client
        self.url_manager = url_manager
        self.user_id = 1
        yield

    async def test_with_no_words_should_return_200_and_empty_list(self):
        resp = self.do_request()
        assert resp.status_code == 200
        wors_dict_list = resp.json()
        assert isinstance(wors_dict_list, list)
        assert len(wors_dict_list) == 0

    async def test_with_one_user_id_should_return_200_and_list_of_words(self):
        word1 = gen_word_object(text='text1', user_id=self.user_id)
        word2 = gen_word_object(text='text2', user_id=self.user_id)

        id1 = await self.session.words.create(word1)
        id2 = await self.session.words.create(word2)

        resp = self.do_request()
        assert resp.status_code == 200
        wors_dict_list = resp.json()
        assert isinstance(wors_dict_list, list)
        assert len(wors_dict_list) == 2

        word_dicts_by_id = {word_dict['id']: word_dict for word_dict in wors_dict_list}
        assert str(id1) in word_dicts_by_id
        assert str(id2) in word_dicts_by_id

        assert_dict_with_word_object(wors_dict_list[0], word1)
        assert_dict_with_word_object(wors_dict_list[1], word2)

    async def test_with_multiple_user_ids_should_return_200_and_list_of_words_for_given_user_id(self):
        other_user_id = 2
        word1 = gen_word_object(text='text1', user_id=self.user_id)
        word2 = gen_word_object(text='text2', user_id=self.user_id)
        other_user_word = gen_word_object(text='other_user_text', user_id=other_user_id)

        id1 = await self.session.words.create(word1)
        id2 = await self.session.words.create(word2)
        await self.session.words.create(other_user_word)

        resp = self.do_request()
        assert resp.status_code == 200
        wors_dict_list = resp.json()
        assert isinstance(wors_dict_list, list)
        assert len(wors_dict_list) == 2

        word_dicts_by_id = {word_dict['id']: word_dict for word_dict in wors_dict_list}
        assert str(id1) in word_dicts_by_id
        assert str(id2) in word_dicts_by_id

        assert_dict_with_word_object(wors_dict_list[0], word1)
        assert_dict_with_word_object(wors_dict_list[1], word2)

    def do_request(self):
        return self.api_client.get(self.url_manager.get_words_url(user_id=self.user_id))