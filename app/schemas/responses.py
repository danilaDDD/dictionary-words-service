from datetime import datetime

from pydantic import BaseModel


class WordResponseEntity(BaseModel):
    id: str
    text: str
    collections: list
    user_id: int
    translations: list
    created_at: datetime
    updated_at: datetime