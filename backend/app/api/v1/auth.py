from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.core.deps import get_current_user
from app.models.user import User
from app.models.organization import Organization, Membership, RoleType, PlanTier
from app.models.agent_config import AgentConfig
from app.models.whatsapp_account import WhatsAppAccount
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, RefreshTokenRequest, UserOut
import re

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user email already exists
    existing = await db.execute(select(User).where(User.email == req.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # Create User
    user = User(
        email=req.email.lower(),
        hashed_password=get_password_hash(req.password),
        full_name=req.full_name,
        phone_number=req.phone_number,
        is_active=True,
    )
    db.add(user)
    await db.flush()

    # Create Organization
    org_slug = re.sub(r"[^a-zA-Z0-9-]", "-", req.organization_name.lower()).strip("-")
    if not org_slug:
        org_slug = f"org-{user.id[:8]}"

    # Ensure unique slug
    slug_check = await db.execute(select(Organization).where(Organization.slug == org_slug))
    if slug_check.scalar_one_or_none():
        org_slug = f"{org_slug}-{user.id[:4]}"

    organization = Organization(
        name=req.organization_name,
        slug=org_slug,
        plan=PlanTier.STARTER.value,
        currency="BDT",
        timezone="Asia/Dhaka",
        is_active=True,
    )
    db.add(organization)
    await db.flush()

    # Create Membership as OWNER
    membership = Membership(
        organization_id=organization.id,
        user_id=user.id,
        role=RoleType.OWNER.value,
    )
    db.add(membership)

    # Initialize Default Agent Configuration
    agent_cfg = AgentConfig(
        organization_id=organization.id,
        agent_name="Sales AI",
        personality="Helpful, consultative and energetic digital sales representative",
        tone="Professional, polite and friendly",
        language="English & Bengali (Banglish)",
        greeting_message=f"Hello! Welcome to {organization.name}. How can I assist you today? 🛍️",
        business_description=f"{organization.name} online sales store.",
        shipping_rules="Dhaka: ৳60 (24-48 hours), Outside Dhaka: ৳120 (2-4 days).",
        return_policy="7-day hassle-free exchange and return policy.",
    )
    db.add(agent_cfg)

    # Initialize WhatsApp Account Placeholder
    wa_account = WhatsAppAccount(
        organization_id=organization.id,
        webhook_verify_token="sales_ai_webhook_verify_secret",
        status="CONNECTED",
    )
    db.add(wa_account)

    await db.commit()

    access_token = create_access_token(subject=user.id, organization_id=organization.id)
    refresh_token = create_refresh_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        organization_id=organization.id,
        organization_name=organization.name,
        role=membership.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email.lower()))
    user = result.scalar_one_or_none()

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    # Find organization membership
    mem_result = await db.execute(
        select(Membership, Organization)
        .join(Organization, Membership.organization_id == Organization.id)
        .where(Membership.user_id == user.id, Organization.is_active == True)
    )
    first_mem = mem_result.first()
    if not first_mem:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No active organization associated with this user.",
        )

    membership, org = first_mem
    access_token = create_access_token(subject=user.id, organization_id=org.id)
    refresh_token = create_refresh_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        organization_id=org.id,
        organization_name=org.name,
        role=membership.role,
    )


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
