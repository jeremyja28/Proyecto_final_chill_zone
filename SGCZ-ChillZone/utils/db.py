import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from config import Config

_pool = None

def init_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="chill_zone_pool",
            pool_size=10,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )

@contextmanager
def get_conn():
    if _pool is None:
        init_pool()
    conn = _pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_cursor(dictionary=True):
    with get_conn() as conn:
        cursor = conn.cursor(dictionary=dictionary, buffered=True)
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


def query_all(sql: str, params: tuple = ()): 
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def query_one(sql: str, params: tuple = ()): 
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute(sql: str, params: tuple = ()): 
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.lastrowid
