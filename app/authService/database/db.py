from psycopg import connect
from psycopg.rows import dict_row

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_db_connection():
    return connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row,
    )
