import sqlite3

def get_connection():
    conn = sqlite3.connect('db/games.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all(sql, params=None):
    """Execute query and return all results"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def fetch_one(sql, params=None):
    """Execute query and return one result"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def execute_query(sql, params=None):
    """Execute INSERT/UPDATE/DELETE and return lastrowid"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id