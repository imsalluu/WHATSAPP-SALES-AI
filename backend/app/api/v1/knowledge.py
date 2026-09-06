from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.deps import get_current_organization, require_roles
from app.models.organization import Organization, RoleType
from app.models.knowledge import KnowledgeDocument
from app.schemas.knowledge import DocumentCreate, DocumentOut, SearchKnowledgeRequest, SearchKnowledgeResult
from app.rag.service import RAGService

router = APIRouter(prefix="/knowledge", tags=["RAG Knowledge Base"])


@router.get("/documents", response_model=List[DocumentOut])
async def list_documents(
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(KnowledgeDocument).where(
        KnowledgeDocument.organization_id == current_org.id
    ).order_by(KnowledgeDocument.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/documents", response_model=DocumentOut)
async def create_document(
    data: DocumentCreate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    rag = RAGService(db=db, organization_id=current_org.id)
    doc = await rag.ingest_document(
        title=data.title,
        content=data.content,
        document_type=data.document_type,
        source_url=data.source_url,
    )
    await db.commit()
    await db.refresh(doc)
    return doc


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    stmt = select(KnowledgeDocument).where(
        KnowledgeDocument.id == document_id,
        KnowledgeDocument.organization_id == current_org.id,
    )
    res = await db.execute(stmt)
    doc = res.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
    await db.commit()
    return {"message": "Knowledge document deleted"}


@router.post("/search", response_model=List[SearchKnowledgeResult])
async def search_knowledge(
    req: SearchKnowledgeRequest,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    rag = RAGService(db=db, organization_id=current_org.id)
    results = await rag.search(query=req.query, limit=req.limit)
    return results
