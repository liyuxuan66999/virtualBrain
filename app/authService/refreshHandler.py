from fastapi import HTTPException, status
import jwt

from config import JWT_ALGORITHM, JWT_SECRET
from database import find_user_by_email
from httpResponseTemplates.error_templates import (
    INVALID_EMAIL_OR_PASSWORD,
    TOKEN_ERROR,
)
from models import RefreshTokenRequest
from utils import create_access_token


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

    user = find_user_by_email(decoded["email"])
    if user is None or user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_EMAIL_OR_PASSWORD,
        )

    new_access_token = create_access_token(
        user_id=str(user["id"]),
        email=user["email"],
    )

    return {
        "message": "Access token refreshed",
        "token": {
            "access_token": new_access_token,
            "token_type": "bearer",
        },
    }
