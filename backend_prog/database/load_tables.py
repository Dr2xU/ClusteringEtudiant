import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_prog')))

from database.connection import get_connection
from database.create_tables import create_all_tables


def check_tables_exist(conn):
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users';"
    )
    return cursor.fetchone() is not None

def load_users(conn):
    cursor = conn.execute("SELECT * FROM users;")
    return cursor.fetchall()

def load_elections(conn):
    cursor = conn.execute("SELECT * FROM elections;")
    return cursor.fetchall()

def load_election_participants(conn):
    cursor = conn.execute("SELECT * FROM election_participants;")
    return cursor.fetchall()

def load_election_groups(conn):
    cursor = conn.execute("SELECT * FROM election_groups;")
    return cursor.fetchall()

def load_group_members(conn):
    cursor = conn.execute("SELECT * FROM group_members;")
    return cursor.fetchall()

def load_student_votes(conn):
    cursor = conn.execute("SELECT * FROM student_votes;")
    return cursor.fetchall()

def load_election_votes(conn):
    cursor = conn.execute("SELECT * FROM election_votes;")
    return cursor.fetchall()

def load_all_data():
    conn = get_connection()
    if not check_tables_exist(conn):
        print("Tables not found, creating all tables...")
        create_all_tables(conn)

    data = {
        "users": load_users(conn),
        "elections": load_elections(conn),
        "election_participants": load_election_participants(conn),
        "election_groups": load_election_groups(conn),
        "group_members": load_group_members(conn),
        "student_votes": load_student_votes(conn),
        "election_votes": load_election_votes(conn),
    }
    conn.close()
    return data

if __name__ == "__main__":

    all_data = load_all_data()
    
    for table, rows in all_data.items():
        print(f"Table: {table}, Rows: {len(rows)}")
