from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class KnowledgeChunkOut(BaseModel):
    id: str
    chunk_index: int
    content: str
    chunk_metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    title: str
    document_type: str = "GENERAL"
    content: str
    source_url: Optional[str] = None


class DocumentOut(BaseModel):
    id: str
    organization_id: str
    title: str
    document_type: str
    source_url: Optional[str] = None
    total_chunks: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SearchKnowledgeRequest(BaseModel):
    query: str
    limit: int = 4


class SearchKnowledgeResult(BaseModel):
    chunk_id: str
    document_title: str
    document_type: str
    content: str
    score: float
