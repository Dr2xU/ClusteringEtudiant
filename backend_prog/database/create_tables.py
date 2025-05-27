from database.connection import get_connection

conn = get_connection()

def create_users_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('student', 'teacher', 'admin')) NOT NULL
        );
    ''')

def create_elections_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS elections (
            election_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_by_teacher_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (created_by_teacher_id) REFERENCES users(user_id)
        );
    ''')

def create_election_participants_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS election_participants (
            election_id INTEGER NOT NULL,
            student_user_id TEXT NOT NULL,
            PRIMARY KEY (election_id, student_user_id),
            FOREIGN KEY (election_id) REFERENCES elections(election_id),
            FOREIGN KEY (student_user_id) REFERENCES users(user_id)
        );
    ''')

def create_election_groups_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS election_groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            election_id INTEGER NOT NULL,
            FOREIGN KEY (election_id) REFERENCES elections(election_id)
        );
    ''')

def create_group_members_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            group_id INTEGER NOT NULL,
            student_user_id TEXT NOT NULL,
            PRIMARY KEY (group_id, student_user_id),
            FOREIGN KEY (group_id) REFERENCES election_groups(group_id),
            FOREIGN KEY (student_user_id) REFERENCES users(user_id)
        );
    ''')

def create_student_votes_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS student_votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            election_id INTEGER NOT NULL,
            voter_user_id TEXT NOT NULL,
            candidate_user_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (election_id) REFERENCES elections(election_id),
            FOREIGN KEY (voter_user_id) REFERENCES users(user_id),
            FOREIGN KEY (candidate_user_id) REFERENCES users(user_id)
        );
    ''')

def create_election_votes_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS election_votes (
            election_id INTEGER NOT NULL,
            vote_id INTEGER NOT NULL,
            PRIMARY KEY (election_id, vote_id),
            FOREIGN KEY (election_id) REFERENCES elections(election_id),
            FOREIGN KEY (vote_id) REFERENCES student_votes(vote_id)
        );
    ''')

def create_all_tables(conn):
    create_users_table(conn)
    create_elections_table(conn)
    create_election_participants_table(conn)
    create_election_groups_table(conn)
    create_group_members_table(conn)
    create_student_votes_table(conn)
    create_election_votes_table(conn)
    conn.commit()
