import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_prog')))

from database.connection import get_connection

def get_user_by_email_password(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, email, role FROM users
        WHERE email = ? AND password = ?;
    ''', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user