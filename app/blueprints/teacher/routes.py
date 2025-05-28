import sys
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services import (
    create_election, list_elections_by_teacher, get_election_by_id,
    update_election_status, delete_election,
    list_all_students,
    get_teacher_by_id, 
    update_teacher_profile,
    update_teacher_password, run_full_grouping
)

from app.models import Student, StudentVote
from app.dao import get_groups_by_election, get_members_by_group

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

from functools import wraps

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'teacher':
            flash("You must be logged in as a teacher to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@teacher_bp.route('/')
@teacher_required
def dashboard():
    """
    Teacher dashboard that lists all elections created by the logged-in teacher.
    """
    teacher_id = session.get('user_id')
    teacher = get_teacher_by_id(teacher_id)
    elections = list_elections_by_teacher(teacher_id)
    return render_template('teacher/dashboard.html', elections=elections, teacher=teacher)

@teacher_bp.route('/election/new', methods=['GET', 'POST'])
@teacher_required
def create_new_election():
    """
    Create a new election. On GET, show form. On POST, save it.
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        group_size = int(request.form['students_per_group'])
        teacher_id = session.get('user_id')
        selected_student_ids = request.form.getlist('student_ids')  # list of strings
        selected_student_ids = list(map(int, selected_student_ids))

        create_election(
            title=title,
            start_date=start_date,
            end_date=end_date,
            teacher_id=teacher_id,
            students_per_group=group_size,
            description=description,
            student_ids=selected_student_ids
        )

        flash('Election created successfully.', 'success')
        return redirect(url_for('teacher.dashboard'))
    else:
        students = list_all_students()  # get all students for selection
        return render_template('teacher/election_form.html', students=students)

@teacher_bp.route('/complete-profile', methods=['GET', 'POST'])
@teacher_required
def complete_profile():
    teacher_id = session.get('user_id')
    teacher = get_teacher_by_id(teacher_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name')         
        last_name = request.form.get('last_name')
        department = request.form.get('department')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password != password_confirm:
            flash("Passwords do not match.", "danger")
            return render_template('teacher/complete_profile.html', teacher=teacher)

        # Update profile info and optionally password
        update_teacher_profile(teacher_id, first_name, last_name, department)
        if password:
            update_teacher_password(teacher_id, password)

        flash("Profile updated successfully.", "success")
        return redirect(url_for('teacher.dashboard'))

    return render_template('teacher/complete_profile.html', teacher=teacher)


@teacher_bp.route('/election/<int:election_id>/manage')
@teacher_required
def manage_election(election_id):
    """
    View and manage a specific election (students, votes, status).
    """
    election = get_election_by_id(election_id)
    return render_template('teacher/manage_election.html', election=election)

@teacher_bp.route('/election/<int:election_id>/delete')
@teacher_required
def delete_election_route(election_id):
    """
    Delete an election.
    """
    if delete_election(election_id):
        flash("Election deleted.", "info")
    else:
        flash("Failed to delete election.", "danger")
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/election/<int:election_id>/status/<string:status>')
@teacher_required
def change_election_status(election_id, status):
    """
    Change the status of an election (e.g., pause, finish, resume).
    """
    if update_election_status(election_id, status):
        flash(f"Election status updated to '{status}'.", "success")
    else:
        flash("Failed to update election status.", "danger")
    return redirect(url_for('teacher.manage_election', election_id=election_id))

@teacher_bp.route('/election/<int:election_id>/generate-groups')
@teacher_required
def generate_groups(election_id):
    election = get_election_by_id(election_id)
    if not election:
        flash("Election not found.", "danger")
        return redirect(url_for('teacher.dashboard'))

    students = [s.id for s in election.students]
    group_size = election.students_per_group

    if len(students) < group_size:
        flash(f"Not enough students to form a group (need at least {group_size}).", "warning")
        return redirect(url_for('teacher.manage_election', election_id=election_id))

    try:
        student_to_group, score, groups_to_highlight, total_satisfaction, avg_satisfaction = run_full_grouping(
            election_id, students, group_size
        )
        flash(f"Groups generated (Affinity Score: {score:.2f}, Satisfaction Score: {total_satisfaction:.2f}).", "success")
    except Exception as e:
        flash(f"Error during group formation: {str(e)}", "danger")
        return redirect(url_for('teacher.manage_election', election_id=election_id))

    return redirect(url_for('teacher.view_groups', election_id=election_id))


@teacher_bp.route('/election/<int:election_id>/groups')
@teacher_required
def view_groups(election_id):
    election = get_election_by_id(election_id)
    groups = get_groups_by_election(election_id)

    # Get all votes for this election (list of StudentVote)
    votes = StudentVote.query.filter_by(election_id=election_id).all()

    # Build a mapping: voter_id -> dict of candidate_id -> score
    votes_map = {}
    for vote in votes:
        votes_map.setdefault(vote.voter_id, {})[vote.candidate_id] = vote.score

    group_data = []
    for group in groups:
        members = get_members_by_group(group.id)
        students = [Student.query.get(m.student_id) for m in members]

        member_ids = {m.student_id for m in members}
        highlight = False

        for student in students:
            voted_candidates = votes_map.get(student.id, {})
            if set(voted_candidates.keys()).intersection(member_ids - {student.id}):
                highlight = True
                break

        group_data.append({
            'group': group,
            'members': students,
            'highlight': highlight
        })

    return render_template('teacher/view_groups.html',
                           election=election,
                           group_data=group_data,
                           votes_map=votes_map)
