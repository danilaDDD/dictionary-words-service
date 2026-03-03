from typing import List

import pymongo
from bson import ObjectId
from fastapi import HTTPException
from fastapi.params import Depends
from pymongo.errors import WriteError

from app.db.session_manager import SessionManager, get_session_manager
from app.schemas.requests import CreateWordRequest, UpdateWordRequest
from app.schemas.responses import WordResponseEntity


class RestWordService:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def create_word(self, user_id: int, request: CreateWordRequest) -> WordResponseEntity:
        try:
            async with self.session_manager.start() as session:
                word = request.get_word(user_id)
                obj_id = await session.words.create(word)
                word = await session.words.find_by_id(obj_id)

                return WordResponseEntity.of(word)

        except WriteError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_word(self, user_id: int, word_id: str,
                          request: UpdateWordRequest) -> WordResponseEntity:
        if request.is_empty():
            raise HTTPException(status_code=400, detail="At least one field must be provided for update.")

        async with self.session_manager.start() as session:
            id_obj = ObjectId(word_id)
            word = await session.words.find_by_id(id_obj)

            if word is None:
                self._raise_not_found_exception()

            if word.user_id != user_id:
                self._raise_unauthorized_exception()

            if request.collections is not None:
                word.collections = request.collections
            if request.translations is not None:
                word.translations = request.translations

            await session.words.update(id_obj, word)
            saved_word = await session.words.find_by_id(id_obj)

            return WordResponseEntity.of(saved_word)

    async def get_words(self, user_id: int) -> List[WordResponseEntity]:
        async with self.session_manager.start() as session:
            words = await session.words.find_by_user_id(user_id)
            return [WordResponseEntity.of(word) for word in words]

    async def get_word_by_id(self, id: str, user_id: int) -> WordResponseEntity:
        pass

    async def delete_word(self, id: str) -> WordResponseEntity:
        pass

    def _raise_unauthorized_exception(self):
        raise HTTPException(status_code=403, detail="Unauthorized to access this resource.")

    def _raise_not_found_exception(self):
        raise HTTPException(status_code=404, detail="Word not found.")


def get_rest_word_service(session_manager: SessionManager = Depends(get_session_manager)) -> RestWordService:
    return RestWordService(session_manager)