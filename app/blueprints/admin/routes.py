import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.services import (
    create_teacher, list_all_teachers,
    create_student, list_all_students,
    delete_teacher, delete_student  # <-- import delete services
)
import datetime
import random
import string
from app.models import Teacher, Student
from app.extensions import db  # needed for rollback on error

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def generate_unique_id():
    year = datetime.datetime.now().year
    while True:
        digits = ''.join(random.choices(string.digits, k=6))
        candidate_id = f"{year}{digits}"
        # Check existence in DB for uniqueness
        exists = Teacher.query.filter_by(unique_id=candidate_id).first() or \
                 Student.query.filter_by(unique_id=candidate_id).first()
        if not exists:
            return candidate_id


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

@admin_bp.route('/')
def dashboard():
    """Redirect to teachers list by default."""
    return redirect(url_for('admin.view_teachers'))

@admin_bp.route('/teachers')
def view_teachers():
    """View all registered teachers."""
    teachers = list_all_teachers()
    return render_template('admin/users.html', users=teachers, role='teacher')

@admin_bp.route('/students')
def view_students():
    """View all registered students."""
    students = list_all_students()
    return render_template('admin/users.html', users=students, role='student')

@admin_bp.route('/add/<role>', methods=['GET', 'POST'])
def add_user(role):
    if request.method == 'POST':
        unique_id = request.form.get('unique_id')  # read unique_id from form!
        email = request.form['email']
        password = request.form['password']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')

        try:
            if role == 'teacher':
                department = request.form.get('department', '')
                create_teacher(email, password, first_name, last_name, department, unique_id)
            elif role == 'student':
                class_name = request.form.get('class_name', '')
                section = request.form.get('section', '')
                create_student(email, password, first_name, last_name, class_name, section, unique_id)
            else:
                flash('Invalid role', 'error')
                return redirect(url_for('admin.dashboard'))

            flash(f'{role.capitalize()} added successfully!', 'success')
            return redirect(url_for(f'admin.view_{role}s'))

        except Exception as e:
            flash(f'Error creating {role}: {str(e)}', 'danger')

    # GET request: generate credentials and send to template
    if role not in ['teacher', 'student']:
        flash('Invalid role specified.', 'danger')
        return redirect(url_for('admin.dashboard'))

    unique_id = generate_unique_id()
    email = f"{unique_id}@jwc.com"
    password = generate_password()

    return render_template(
        'admin/user_form.html',
        role=role,
        unique_id=unique_id,
        email=email,
        password=password
    )

@admin_bp.route('/delete/<role>/<int:user_id>', methods=['POST'])
def delete_user(role, user_id):
    if role not in ['teacher', 'student']:
        flash('Invalid role specified.', 'danger')
        return redirect(url_for('admin.dashboard'))

    try:
        if role == 'teacher':
            success = delete_teacher(user_id)
        else:
            success = delete_student(user_id)

        if success:
            flash(f'{role.capitalize()} deleted successfully.', 'success')
        else:
            flash(f'{role.capitalize()} not found.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting {role}: {str(e)}', 'danger')

    return redirect(url_for(f'admin.view_{role}s'))
