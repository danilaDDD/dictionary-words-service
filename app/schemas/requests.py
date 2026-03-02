from typing import List, Optional

from pydantic import BaseModel

from app.models.models import Collection, Word


class CreateWordRequest(BaseModel):
    text: str
    collections: List[Collection]
    translations: List[str]

    def get_word(self, user_id: int) -> Word:
        return Word(text=self.text,
                    user_id=user_id,
                    collections=self.collections,
                    translations=self.translations)


class UpdateWordRequest(BaseModel):
    collections: Optional[List[Collection]] = None
    translations: Optional[List[str]] = None

    def is_empty(self) -> bool:
        return self.collections is None and self.translations is None