from typing import List

from fastapi.params import Depends

from app.db.session_manager import SessionManager, get_session_manager
from app.schemas.requests import CreateWordRequest, UpdateWordRequest
from app.schemas.responses import WordResponseEntity


class RestWordService:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def create_chat(self, request: CreateWordRequest) -> WordResponseEntity:
        pass

    async def update_word(self, request: UpdateWordRequest) -> WordResponseEntity:
        pass

    async def get_words(self) -> List[WordResponseEntity]:
        pass

    async def get_word_by_id(self, id: str) -> WordResponseEntity:
        pass

    async def delete_word(self, id: str) -> WordResponseEntity:
        pass


def get_rest_word_service(session_manager: SessionManager = Depends(get_session_manager)) -> RestWordService:
    return RestWordService(session_manager)