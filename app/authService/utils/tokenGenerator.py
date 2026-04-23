from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt

from config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

def create_access_token(user_id: str, email: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# use refresh token to call refresh service enable access token 
# auto extension
def create_refresh_token(user_id: str, email: str) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # jti: for refresh token revocation and 
    # rotation (every refresh will revoke old refresh token)
    # jti will be passed to client use as current token identifier
    # * id cannot be used because it will reveal DB hash strategy
    jti = str(uuid4())

    payload = {
        "sub": user_id,
        "email": email,
        "type": "refresh",
        "jti":jti,
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token, jti, expire