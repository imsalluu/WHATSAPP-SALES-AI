from sqlalchemy import Column, String, ForeignKey, JSON, Text, Integer
from sqlalchemy.orm import relationship
import enum
from app.models.base import TenantModel


class DocumentType(str, enum.Enum):
    POLICY = "POLICY"
    FAQ = "FAQ"
    MANUAL = "MANUAL"
    SHIPPING = "SHIPPING"
    RETURN_REFUND = "RETURN_REFUND"
    GENERAL = "GENERAL"


class DocumentStatus(str, enum.Enum):
    PENDING = "PENDING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class KnowledgeDocument(TenantModel):
    __tablename__ = "knowledge_documents"

    title = Column(String(255), nullable=False)
    document_type = Column(String(50), default=DocumentType.GENERAL.value, nullable=False)
    source_url = Column(String(1024), nullable=True)
    raw_content = Column(Text, nullable=False)
    total_chunks = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default=DocumentStatus.INDEXED.value, nullable=False)

    # Relationships
    chunks = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")


class KnowledgeChunk(TenantModel):
    __tablename__ = "knowledge_chunks"

    document_id = Column(String(36), ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, default=0, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)  # List[float] embedding (1536 dim)
    chunk_metadata = Column(JSON, default=dict, nullable=False)

    # Relationships
    document = relationship("KnowledgeDocument", back_populates="chunks")
