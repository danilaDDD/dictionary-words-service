import pytest

from app.db.session_manager import SessionManager
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.db
class TestSessionManager:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, session: SessionManager) -> None:
        self.session = session

    async def test_1_operation(self):
        word = gen_word_object('test')

        session = self.session.start()
        await session.words.create(word)

    async def test_operation_after_close_session(self):
        session = self.session.start()
        word = gen_word_object('test')
        id_obj = await session.words.create(word)

        word.text = 'updated'
        await session.words.update(id_obj, word)




