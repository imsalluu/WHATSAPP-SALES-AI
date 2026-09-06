from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk, DocumentStatus
from app.rag.chunker import RecursiveCharacterChunker
from app.rag.embeddings import EmbeddingService, cosine_similarity


class RAGService:
    def __init__(self, db: AsyncSession, organization_id: str):
        self.db = db
        self.organization_id = organization_id
        self.chunker = RecursiveCharacterChunker(chunk_size=400, chunk_overlap=80)
        self.embedder = EmbeddingService()

    async def ingest_document(
        self,
        title: str,
        content: str,
        document_type: str = "GENERAL",
        source_url: Optional[str] = None,
    ) -> KnowledgeDocument:
        """Chunks, embeds, and stores a document."""
        doc = KnowledgeDocument(
            organization_id=self.organization_id,
            title=title,
            document_type=document_type,
            raw_content=content,
            source_url=source_url,
            status=DocumentStatus.INDEXED.value,
        )
        self.db.add(doc)
        await self.db.flush()

        chunks_text = self.chunker.split_text(content)
        doc.total_chunks = len(chunks_text)

        for idx, chunk_str in enumerate(chunks_text):
            embedding = await self.embedder.get_embedding(chunk_str)
            chunk = KnowledgeChunk(
                organization_id=self.organization_id,
                document_id=doc.id,
                chunk_index=idx,
                content=chunk_str,
                embedding=embedding,
                chunk_metadata={"title": title, "type": document_type},
            )
            self.db.add(chunk)

        await self.db.flush()
        return doc

    async def search(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Hybrid search combining keyword matching and vector similarity."""
        query_embedding = await self.embedder.get_embedding(query)

        stmt = select(KnowledgeChunk, KnowledgeDocument).join(
            KnowledgeDocument, KnowledgeChunk.document_id == KnowledgeDocument.id
        ).where(
            KnowledgeChunk.organization_id == self.organization_id
        )
        result = await self.db.execute(stmt)
        rows = result.all()

        scored_results = []
        query_terms = query.lower().split()

        for chunk, doc in rows:
            # 1. Cosine similarity
            cos_sim = cosine_similarity(query_embedding, chunk.embedding or [])
            
            # 2. Keyword overlap boost
            content_lower = chunk.content.lower()
            keyword_matches = sum(1 for term in query_terms if term in content_lower)
            keyword_score = keyword_matches / max(len(query_terms), 1)

            final_score = (cos_sim * 0.7) + (keyword_score * 0.3)

            scored_results.append({
                "chunk_id": chunk.id,
                "document_title": doc.title,
                "document_type": doc.document_type,
                "content": chunk.content,
                "score": round(final_score, 4),
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:limit]
