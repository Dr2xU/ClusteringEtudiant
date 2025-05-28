import sys
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services import (
    authenticate_admin,
    authenticate_teacher,
    authenticate_student
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_profile_incomplete(user, role):
    # For teachers: first_name, last_name, department required
    if role == 'teacher':
        return not (user.first_name or user.last_name or user.department)
    # For students: first_name, last_name, class_name, section required
    if role == 'student':
        return not (user.first_name or user.last_name or user.class_name or user.section)
    return False

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    General login page for all roles: admin, teacher, student.
    On POST, attempts to authenticate and redirect to the appropriate dashboard.
    """

    # Redirect logged-in users away from login page
    if 'user_id' in session and 'role' in session:
        role = session['role']
        return redirect(url_for(f'{role}.dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Role-based authentication
        if role == 'admin':
            user = authenticate_admin(email, password)
        elif role == 'teacher':
            user = authenticate_teacher(email, password)
        elif role == 'student':
            user = authenticate_student(email, password)
        else:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.login'))

        # If authentication is successful
        if user:
            session['user_id'] = user.id
            session['role'] = role
            session['email'] = user.email

            if role in ['teacher', 'student'] and is_profile_incomplete(user, role):
                # Redirect to profile completion page
                return redirect(url_for(f'{role}.complete_profile'))

            flash(f"Logged in as {role}: {user.email}", 'success')
            return redirect(url_for(f'{role}.dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
