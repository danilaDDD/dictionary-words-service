from datetime import datetime

from pydantic import BaseModel

from app.models.models import Word


class WordResponseEntity(BaseModel):
    @classmethod
    def of(cls, word: Word) -> "WordResponseEntity":
        return WordResponseEntity(
            id=str(word.id),
            text=word.text,
            collections=word.collections,
            translations=word.translations,
            user_id=word.user_id,
            created_at=word.created_at,
            updated_at=word.updated_at,
        )

    id: str
    text: str
    collections: list
    user_id: int
    translations: list
    created_at: datetime
    updated_at: datetime
