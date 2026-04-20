from fastapi import FastAPI, HTTPException, status
from httpResponseTemplates.error_templates import (
    ACCOUNT_STATUS_ERROR,
    INVALID_EMAIL_OR_PASSWORD,
)
from models import LoginRequest
from database import find_user_by_email, update_last_login
from utils import create_access_token, verify_password

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"hello": "world"}


@app.post("/login")
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
            "token_type": "bearer",
        },
    }
