from fastapi import HTTPException, status

from database import create_user, find_user_by_email
from httpResponseTemplates.error_templates import EMAIL_ALREADY_REGISTERED
from models import RegisterRequest
from utils import hash_password


async def register(payload: RegisterRequest) -> dict:
    normalized_email = payload.email.lower()

    existing_user = find_user_by_email(normalized_email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=EMAIL_ALREADY_REGISTERED,
        )

    password_hash = hash_password(payload.password)
    user = create_user(
        email=normalized_email,
        password_hash=password_hash,
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": str(user["id"]),
            "email": user["email"],
            "email_verified": user["email_verified"],
            "status": user["status"],
            "created_at": user["created_at"],
        },
    }
