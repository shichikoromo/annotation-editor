from pydantic import BaseModel
from typing import Optional

class AIFArgumentInput(BaseModel):
    sentence_id: int
    type: str
    supports: Optional[int]

