from fastapi import HTTPException, status

from database import (
    find_user_by_email,
    update_last_login,
    create_refresh_token_record,
)
from httpResponseTemplates.error_templates import (
    ACCOUNT_STATUS_ERROR,
    INVALID_EMAIL_OR_PASSWORD,
)
from models import LoginRequest
from utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
    hash_token,
)


async def login(payload: LoginRequest) -> dict:
    user = find_user_by_email(payload.email)

    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_EMAIL_OR_PASSWORD,
        )

    if user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ACCOUNT_STATUS_ERROR["inactive"],
        )

    update_last_login(str(user["id"]))

    access_token = create_access_token(
        user_id=str(user["id"]),
        email=user["email"],
    )
    refresh_token, refresh_jti, refresh_expires_at = create_refresh_token(
        user_id=str(user["id"]),
        email=user["email"],
    )

    create_refresh_token_record(
        user_id=str(user["id"]),
        jti=refresh_jti,
        token_hash=hash_token(refresh_token),
        expires_at=refresh_expires_at,
    )

    return {
        "message": "Login successful",
        "user": {
            "id": str(user["id"]),
            "email": user["email"],
            "email_verified": user["email_verified"],
            "status": user["status"],
        },
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    }
