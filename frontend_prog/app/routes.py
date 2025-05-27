from flask import Blueprint, render_template, request, redirect, url_for, session
import sys
import os
import os
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend_prog'))
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

from database.load_tables import load_all_data
from database.save_tables import save_user
from users.user import User

main = Blueprint('main', __name__)
data = load_all_data()
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/students')
def students():
    if 'user' not in session or session['user']['role'] != 'student':
        return redirect(url_for('main.login'))
    return render_template('students.html')

@main.route('/teachers')
def teachers():
    if 'user' not in session or session['user']['role'] != 'teacher':
        return redirect(url_for('main.login'))
    return render_template('teachers.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user1 = User(1234, 'email@hotmail.com', 'password', 'student')

        if user1:
            session['user1'] = {
                'user_id': user1[0],
                'email': user1[1],
                'role': user1[2]
            }

            if user1[2] == 'student':
                return redirect(url_for('main.students'))
            elif user1[2] == 'teacher':
                return redirect(url_for('main.teachers'))
            else:
                error = "Access denied for this role."
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@main.route('/add', methods=['POST'])
def add_user():
    user1 = User(1234, 'email@hotmail.com', 'password', 'student')
    save_user(user1)
    data = load_all_data()
    for table, rows in data.items():
        print(f"Table: {table}, Rows: {len(rows)}")

