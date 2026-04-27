from datetime import datetime, timezone
from typing import Any

from .db import get_db_connection

def create_refresh_token_record(
    user_id: str,
    jti: str,
    token_hash: str,
    expires_at: datetime,
) -> None:
    query = """
        INSERT INTO refresh_tokens (user_id, jti, token_hash, expires_at)
        VALUES (%s, %s, %s, %s)
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id, jti, token_hash, expires_at))
        conn.commit()

def find_refresh_token_by_jti(jti: str) -> dict[str, Any] | None:
    query = """
        SELECT id, user_id, jti, token_hash, expires_at, revoked_at, last_used_at, created_at
        FROM refresh_tokens
        WHERE jti = %s
        LIMIT 1
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (jti,))
            return cur.fetchone()
        
def revoke_refresh_token_by_jti(jti: str) -> None:
    query = """
        UPDATE refresh_tokens
        SET revoked_at = NOW()
        WHERE jti = %s AND revoked_at IS NULL
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (jti,))
        conn.commit()

def touch_refresh_token(jti: str) -> None:
    query = """
        UPDATE refresh_tokens
        SET last_used_at = NOW()
        WHERE jti = %s
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (jti,))
        conn.commit()

def revoke_all_refresh_tokens_for_user(user_id: str) -> None:
    query = """
        UPDATE refresh_tokens
        SET revoked_at = NOW()
        WHERE user_id = %s AND revoked_at IS NULL
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))
        conn.commit()
