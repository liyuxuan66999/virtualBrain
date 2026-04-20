from typing import Any

from .db import get_db_connection


def find_user_by_email(email: str) -> dict[str, Any] | None:
    query = """
        SELECT id, email, password_hash, status, email_verified
        FROM users
        WHERE email = %s
        LIMIT 1
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (email.lower(),))
            return cur.fetchone()


def update_last_login(user_id: str) -> None:
    query = """
        UPDATE users
        SET last_login_at = NOW(),
            updated_at = NOW()
        WHERE id = %s
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))
        conn.commit()
