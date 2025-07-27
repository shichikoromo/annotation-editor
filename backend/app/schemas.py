from pydantic import BaseModel

class RDFAnnotationInput(BaseModel):
    sentence_id: int
    subject: str
    predicate: str
    object_: str
    sentence: str

class AIFAnnotationInput(BaseModel):
    sentence_id: int
    type: str
    supports: str

