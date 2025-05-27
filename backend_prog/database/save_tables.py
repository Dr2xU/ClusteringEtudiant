# db/save_tables.py
from database.connection import get_connection

def save_user(user):
    """
    user = {
        'user_id': str,
        'email': str,
        'password': str,
        'role': str ('student', 'teacher', 'admin')
    }
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, email, password, role)
        VALUES (?, ?, ?, ?);
    ''', (user['user_id'], user['email'], user['password'], user['role']))
    conn.commit()
    conn.close()

def save_election(election):
    """
    election = {
        'id': int or None,
        'teacher_id': str,
        'start_date': str,
        'end_date': str
    }
    """
    conn = get_connection()
    cursor = conn.cursor()
    if election.get('id') is None:
        cursor.execute('''
            INSERT INTO elections (teacher_id, start_date, end_date)
            VALUES (?, ?, ?);
        ''', (election['teacher_id'], election['start_date'], election['end_date']))
        election['id'] = cursor.lastrowid
    else:
        cursor.execute('''
            UPDATE elections SET teacher_id=?, start_date=?, end_date=?
            WHERE id=?;
        ''', (election['teacher_id'], election['start_date'], election['end_date'], election['id']))
    conn.commit()
    conn.close()
    return election['id']

def save_election_participant(election_id, student_id):
    """
    Links a student to an election
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO election_participants (election_id, student_id)
        VALUES (?, ?);
    ''', (election_id, student_id))
    conn.commit()
    conn.close()

def save_election_group(election_id, group_id):
    """
    Links a group to an election
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO election_groups (election_id, group_id)
        VALUES (?, ?);
    ''', (election_id, group_id))
    conn.commit()
    conn.close()

def save_group_member(group_id, student_id):
    """
    Links a student to a group
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO group_members (group_id, student_id)
        VALUES (?, ?);
    ''', (group_id, student_id))
    conn.commit()
    conn.close()

def save_student_vote(vote):
    """
    vote = {
        'id': int or None,
        'student_id': str,
        'candidate_id': str,
        'score': int
    }
    """
    conn = get_connection()
    cursor = conn.cursor()
    if vote.get('id') is None:
        cursor.execute('''
            INSERT INTO student_votes (student_id, candidate_id, score)
            VALUES (?, ?, ?);
        ''', (vote['student_id'], vote['candidate_id'], vote['score']))
        vote['id'] = cursor.lastrowid
    else:
        cursor.execute('''
            UPDATE student_votes SET student_id=?, candidate_id=?, score=?
            WHERE id=?;
        ''', (vote['student_id'], vote['candidate_id'], vote['score'], vote['id']))
    conn.commit()
    conn.close()
    return vote['id']

def save_election_vote(election_id, vote_id):
    """
    Links a vote to an election
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO election_votes (election_id, vote_id)
        VALUES (?, ?);
    ''', (election_id, vote_id))
    conn.commit()
    conn.close()
