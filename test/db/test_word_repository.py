import pytest
from pymongo import AsyncMongoClient

from app.repositories.word_repository import WordRepository
from settings.settings import Settings
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.db
class TestWordRepository:
    def reconnect_client(self):
        self.client = AsyncMongoClient(self.settings.get_database_url())
        self.db = self.client.get_database()
        self.collection = self.db.words
        self.repository = WordRepository(self.collection)

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, settings: Settings):
        self.settings = settings
        self.reconnect_client()

    async def test_add_word(self):
        word = gen_word_object('test')
        id_obj = await self.repository.create(word)
        assert id_obj is not None

        saved_words = await self.repository.find_all()
        assert len(saved_words) == 1
        assert saved_words[0].id == str(id_obj)

        await self.client.close()

    async def test_update(self):
        word = gen_word_object('test')
        id_obj = await self.repository.create(word)

        word.text = 'updated'
        updated_resl = await self.repository.update(id_obj, word)
        assert updated_resl is not None

        words = await self.repository.find_all()
        assert len(words) == 1
        updated_word = words[0]
        assert updated_word is not None
        assert updated_word.text == 'updated'
        assert updated_word.id == str(id_obj)

        await self.client.close()

    async def test_find_by_name(self):
        field = 'test'
        word = gen_word_object(field)
        id_obj = await self.repository.create(word)

        found_words = await self.repository.find_all(text=field)
        assert len(found_words) == 1
        assert found_words[0].id == str(id_obj)

        found_word = await self.repository.find_one(text=field)
        assert found_word is not None
        assert found_word.id == str(id_obj)

        not_found_word = await self.repository.find_one(text='not found')
        assert not_found_word is None

        await self.client.close()



