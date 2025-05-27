import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "voting_app.db"

def get_connection():
    """
    Opens a SQLite connection to the local database file.
    Creates the file if it doesn't exist.
    Returns a connection object.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def close_connection(conn):
    """
    Closes the given SQLite connection.
    """
    if conn:
        conn.close()
