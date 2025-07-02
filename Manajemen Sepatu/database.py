import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()
        return cursor.lastrowid

def fetch_all(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        return cursor.fetchall()

def fetch_dataframe(query, params=None):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)
