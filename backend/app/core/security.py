import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from jose import jwt
import bcrypt
from app.core.config import settings


def create_access_token(subject: Union[str, Any], organization_id: Optional[str] = None, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
    }
    if organization_id:
        to_encode["org_id"] = str(organization_id)
        
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pw_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_whatsapp_signature(payload_bytes: bytes, signature_header: Optional[str], app_secret: str) -> bool:
    """
    Verifies WhatsApp Cloud API webhook signature (sha256=<hash>)
    """
    if not signature_header:
        # If in development or mock mode, allow bypass if header missing
        if settings.ENVIRONMENT == "development":
            return True
        return False
    
    parts = signature_header.split("=")
    if len(parts) != 2 or parts[0] != "sha256":
        return False
        
    expected_hash = parts[1]
    calculated_hash = hmac.new(
        key=app_secret.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(calculated_hash, expected_hash)
