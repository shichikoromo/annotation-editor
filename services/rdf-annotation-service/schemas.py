from pydantic import BaseModel
from typing import Optional

class RDFAnnotationInput(BaseModel):
    sentence_id: int
    subject: str
    predicate: str
    object_: str
    sentence: str
