from typing import List

from pydantic import BaseModel

from app.models.base import BaseMongoModel


class Collection(BaseModel):
    id: str
    name: str

class Word(BaseMongoModel):
    text: str
    collections: List[Collection]
    user_id: int
    sent: bool = False
    translations: List[str]