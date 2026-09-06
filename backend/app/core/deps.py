from typing import Optional, List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.organization import Organization, Membership, RoleType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_organization(
    token: Optional[str] = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Organization:
    org_id = None
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            org_id = payload.get("org_id")
        except Exception:
            pass

    if org_id:
        result = await db.execute(
            select(Organization)
            .join(Membership, Membership.organization_id == Organization.id)
            .where(
                Organization.id == org_id,
                Membership.user_id == current_user.id,
                Organization.is_active == True,
            )
        )
        org = result.scalar_one_or_none()
        if org:
            return org

    # Fallback to first active membership
    result = await db.execute(
        select(Organization)
        .join(Membership, Membership.organization_id == Organization.id)
        .where(
            Membership.user_id == current_user.id,
            Organization.is_active == True,
        )
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to any active organization",
        )
    return org


def require_roles(allowed_roles: List[str]) -> Callable:
    async def role_checker(
        current_user: User = Depends(get_current_user),
        current_org: Organization = Depends(get_current_organization),
        db: AsyncSession = Depends(get_db),
    ) -> Membership:
        result = await db.execute(
            select(Membership).where(
                Membership.organization_id == current_org.id,
                Membership.user_id == current_user.id,
            )
        )
        membership = result.scalar_one_or_none()
        if not membership or (membership.role not in allowed_roles and not current_user.is_superuser):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation",
            )
        return membership

    return role_checker
