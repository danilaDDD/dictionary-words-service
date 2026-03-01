from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.models import Collection, Word


class CreateWordRequest(BaseModel):
    text: str
    collections: List[Collection]
    user_id: int
    translations: List[str]

    def get_word(self):
        return Word(text=self.text,
                    user_id=self.user_id,
                    collections=self.collections,
                    translations=self.translations)

class UpdateWordRequest(BaseModel):
    collections: Optional[List[Collection]]
    translations: Optional[List[str]]