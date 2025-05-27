import unittest
from pathlib import Path
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_prog')))

from database.connection import get_connection, close_connection

class TestDatabaseConnection(unittest.TestCase):
    def test_get_connection_opens_db(self):
        conn = get_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        cursor = conn.execute("PRAGMA foreign_keys;")
        fk_status = cursor.fetchone()[0]
        self.assertEqual(fk_status, 1)
        close_connection(conn)

    def test_close_connection(self):
        conn = get_connection()
        close_connection(conn)
        close_connection(conn)
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1;")

if __name__ == "__main__":
    unittest.main()