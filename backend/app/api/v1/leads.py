from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.deps import get_current_organization
from app.models.organization import Organization
from app.models.lead import Lead
from app.schemas.lead import LeadOut, LeadUpdate

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/", response_model=List[LeadOut])
async def list_leads(
    status_filter: Optional[str] = None,
    min_score: Optional[int] = None,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Lead).where(Lead.organization_id == current_org.id)
    if status_filter:
        stmt = stmt.where(Lead.status == status_filter.upper())
    if min_score is not None:
        stmt = stmt.where(Lead.lead_score >= min_score)
    stmt = stmt.order_by(desc(Lead.lead_score), desc(Lead.updated_at))

    res = await db.execute(stmt)
    return res.scalars().all()


@router.patch("/{lead_id}", response_model=LeadOut)
async def update_lead(
    lead_id: str,
    data: LeadUpdate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Lead).where(Lead.id == lead_id, Lead.organization_id == current_org.id)
    res = await db.execute(stmt)
    lead = res.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.name is not None:
        lead.name = data.name
    if data.intent is not None:
        lead.intent = data.intent
    if data.interested_products is not None:
        lead.interested_products = data.interested_products
    if data.budget is not None:
        lead.budget = data.budget
    if data.location is not None:
        lead.location = data.location
    if data.lead_score is not None:
        lead.lead_score = data.lead_score
    if data.status is not None:
        lead.status = data.status.upper()
    if data.notes is not None:
        lead.notes = data.notes

    await db.commit()
    await db.refresh(lead)
    return lead
