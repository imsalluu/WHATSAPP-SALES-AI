from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.deps import get_current_organization, require_roles
from app.models.organization import Organization, RoleType
from app.models.agent_config import AgentConfig
from app.schemas.agent_config import AgentConfigOut, AgentConfigUpdate

router = APIRouter(prefix="/agent-config", tags=["AI Sales Agent Config"])


@router.get("/", response_model=AgentConfigOut)
async def get_agent_config(
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AgentConfig).where(AgentConfig.organization_id == current_org.id)
    res = await db.execute(stmt)
    cfg = res.scalars().first()
    if not cfg:
        cfg = AgentConfig(
            organization_id=current_org.id,
            agent_name="Sales Copilot",
            personality="Friendly, consultative and concise",
            tone="Professional & Helpful",
            language="English / Bengali (Banglish)",
            greeting_message=f"Hello! Welcome to {current_org.name}. How can I help you today? 🛍️",
        )
        db.add(cfg)
        await db.commit()
        await db.refresh(cfg)
    return cfg


@router.put("/", response_model=AgentConfigOut)
async def update_agent_config(
    data: AgentConfigUpdate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    stmt = select(AgentConfig).where(AgentConfig.organization_id == current_org.id)
    res = await db.execute(stmt)
    cfg = res.scalars().first()
    if not cfg:
        cfg = AgentConfig(organization_id=current_org.id)
        db.add(cfg)

    update_dict = data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(cfg, k, v)

    await db.commit()
    await db.refresh(cfg)
    return cfg
