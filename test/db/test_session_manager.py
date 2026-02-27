import pytest

from app.db.session_manager import SessionManager
from app.models.models import Collection, Word
from test.testutils.generation import gen_word_object


@pytest.mark.asyncio
@pytest.mark.db
class TestSessionManager:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager

    async def test_1_operation(self):
        word = gen_word_object('test')

        async with self.session_manager.start() as session:
            await session.words.create(word)

    async def test_operation_after_close_session(self):
        async with self.session_manager.start() as session:
            word = gen_word_object('test')
            id_obj = await session.words.create(word)

        async with self.session_manager.start() as session:
            word.text = 'updated'
            await session.words.update(id_obj, word)




