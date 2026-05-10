from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=15)

class ChunkResult(BaseModel):
    text: str
    score: float

class QuestionResponse(BaseModel):
    answer: str
    source_chunks: list[ChunkResult]

class IngestResponse(BaseModel):
    message: str
    chunks_stored: int
    new_chunks: int