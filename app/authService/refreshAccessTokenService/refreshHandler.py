from datetime import datetime, timezone

from fastapi import HTTPException, status
import jwt

from config import JWT_ALGORITHM, JWT_SECRET
from database import (
    find_user_by_email,
    find_active_refresh_token_by_jti,
    revoke_refresh_token_by_jti,
    touch_refresh_token,
    create_refresh_token_record,
)

from httpResponseTemplates.error_templates import (
    INVALID_EMAIL_OR_PASSWORD,
    TOKEN_ERROR,
)
from models import RefreshTokenRequest
from utils import (
    create_access_token,
    create_refresh_token,
    hash_token,
)


async def refresh_access_token(payload: RefreshTokenRequest) -> dict:
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["refresh_token_expired"],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token"],
        )

    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token_type"],
        )

    refresh_jti = decoded.get("jti")
    if not refresh_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token"],
        )

    token_record = find_active_refresh_token_by_jti(refresh_jti)
    if token_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["refresh_token_not_found"],
        )

    if token_record["revoked_at"] is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["refresh_token_revoked"],
        )

    now = datetime.now(timezone.utc)
    if token_record["expires_at"] <= now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["refresh_token_expired"],
        )

    if token_record["token_hash"] != hash_token(payload.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token"],
        )

    user = find_user_by_email(decoded["email"])
    if user is None or user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_EMAIL_OR_PASSWORD,
        )

    if str(user["id"]) != decoded["sub"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token"],
        )

    touch_refresh_token(refresh_jti)
    revoke_refresh_token_by_jti(refresh_jti)

    new_access_token = create_access_token(
        user_id=str(user["id"]),
        email=user["email"],
    )

    new_refresh_token, new_refresh_jti, new_refresh_expires_at = create_refresh_token(
        user_id=str(user["id"]),
        email=user["email"],
    )

    create_refresh_token_record(
        user_id=str(user["id"]),
        jti=new_refresh_jti,
        token_hash=hash_token(new_refresh_token),
        expires_at=new_refresh_expires_at,
    )

    return {
        "message": "Access token refreshed",
        "token": {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        },
    }
