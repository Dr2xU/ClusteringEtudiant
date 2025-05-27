from flask import Blueprint, render_template, request, redirect, url_for, session
from .db_access import get_user_by_email_password
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_prog')))

from users.user import user

main = Blueprint('main', __name__)
user1 = user(1234, 'truc@mail.com', 'password', 'student')
 
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

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         if user1:
#             session['user1'] = {
#                 'user_id': user1[0],
#                 'email': user1[1],
#                 'role': user1[2]
#             }
#
#             if user1[2] == 'student':
#                 return redirect(url_for('main.students'))
#             elif user1[2] == 'teacher':
#                 return redirect(url_for('main.teachers'))
#             else:
#                 error = "Access denied for this role."
#         else:
#             error = "Invalid email or password."
#
#     return render_template('login.html', error=error)
