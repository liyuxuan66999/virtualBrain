from fastapi import HTTPException, status
import jwt

from config import JWT_ALGORITHM, JWT_SECRET
from database import find_refresh_token_by_jti, revoke_refresh_token_by_jti
from httpResponseTemplates.error_templates import TOKEN_ERROR
from models import LogoutRequest
from utils import hash_token


async def logout(payload: LogoutRequest) -> dict:
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
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
    token_record = find_refresh_token_by_jti(refresh_jti)
    if token_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["refresh_token_not_found"],
        )
    if token_record["token_hash"] != hash_token(payload.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TOKEN_ERROR["invalid_token"],
        )

    revoke_refresh_token_by_jti(refresh_jti)

    return {
        "message": "Logout successful"
    }
