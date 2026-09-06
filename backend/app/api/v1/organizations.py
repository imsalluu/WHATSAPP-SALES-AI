from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_organization, require_roles
from app.models.user import User
from app.models.organization import Organization, Membership, RoleType
from app.schemas.organization import OrganizationOut, OrganizationUpdate, MembershipOut, InviteMemberRequest

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/current", response_model=OrganizationOut)
async def get_current_org(current_org: Organization = Depends(get_current_organization)):
    return current_org


@router.patch("/current", response_model=OrganizationOut)
async def update_current_org(
    update_data: OrganizationUpdate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _membership: Membership = Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    if update_data.name is not None:
        current_org.name = update_data.name
    if update_data.currency is not None:
        current_org.currency = update_data.currency
    if update_data.timezone is not None:
        current_org.timezone = update_data.timezone
    if update_data.logo_url is not None:
        current_org.logo_url = update_data.logo_url

    await db.commit()
    await db.refresh(current_org)
    return current_org


@router.get("/members", response_model=List[MembershipOut])
async def get_team_members(
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Membership, User).join(User, Membership.user_id == User.id).where(
        Membership.organization_id == current_org.id
    )
    res = await db.execute(stmt)
    memberships = []
    for mem, usr in res.all():
        memberships.append(MembershipOut(id=mem.id, role=mem.role, user=usr))
    return memberships
