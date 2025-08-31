from pydantic import BaseModel
from typing import Optional

class AIFArgumentInput(BaseModel):
    source_id: int
    target_id: int
    relation: str
