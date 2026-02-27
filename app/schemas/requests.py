from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.models import Collection


class CreateWordRequest(BaseModel):
    text: str
    collections: List[Collection]
    user_id: int
    translations: List[str]

class UpdateWordRequest(BaseModel):
    collections: Optional[List[Collection]]
    translations: Optional[List[str]]