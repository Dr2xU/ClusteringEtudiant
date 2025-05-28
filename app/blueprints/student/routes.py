import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import (
    get_all_votes_for_election,
    cast_vote,
    delete_votes_by_student,
    get_votes_by_student,
    get_election_by_id
)
from app.models import Student
from app.dao import get_groups_by_election, get_members_by_group
from flask import request, session, redirect, url_for, flash, render_template
from app.services import get_student_by_id, update_student_profile, update_student_password


student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/')
@student_bp.route('/')
def dashboard():
    student_id = session.get('user_id')
    if not student_id:
        flash("Please log in.", "warning")
        return redirect(url_for('auth.login'))
    student = Student.query.get(student_id)
    if not student:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))
    elections = student.elections
    return render_template('student/dashboard.html', elections=elections)

@student_bp.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    student_id = session.get('user_id')
    student = get_student_by_id(student_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        class_name = request.form.get('class_name')
        section = request.form.get('section')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password != password_confirm:
            flash("Passwords do not match.", "danger")
            return render_template('student/complete_profile.html', student=student)

        update_student_profile(student_id, first_name, last_name, class_name, section)
        if password:
            update_student_password(student_id, password)

        flash("Profile updated successfully.", "success")
        return redirect(url_for('student.dashboard'))

    return render_template('student/complete_profile.html', student=student)


@student_bp.route('/election/<int:election_id>/vote', methods=['GET', 'POST'])
def vote(election_id):
    student_id = session.get('user_id')
    election = get_election_by_id(election_id)

    # Allow voting only if election is running or paused (but not finished)
    if election.status == 'finished':
        flash("Voting for this election is closed.", "warning")
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        selected_ids = request.form.getlist('candidate_ids')

        # Server-side validation of max votes
        if len(selected_ids) > election.max_votes_per_student:
            flash(f"You can select up to {election.max_votes_per_student} candidates only.", "danger")
            students = election.students
            existing_votes = get_votes_by_student(election_id, student_id)
            voted_ids = [vote.candidate_id for vote in existing_votes]
            return render_template('student/vote_form.html', election=election, students=students, voted_ids=voted_ids)

        # Delete old votes and save new votes
        delete_votes_by_student(election_id, student_id)
        for index, candidate_id in enumerate(selected_ids):
            score = len(selected_ids) - index
            cast_vote(election_id, student_id, int(candidate_id), score)

        flash("Votes submitted successfully.", "success")
        return redirect(url_for('student.dashboard'))

    # GET method: show vote form
    students = election.students
    existing_votes = get_votes_by_student(election_id, student_id)
    voted_ids = [vote.candidate_id for vote in existing_votes]

    return render_template('student/vote_form.html', election=election, students=students, voted_ids=voted_ids)


@student_bp.route('/election/<int:election_id>/results')
def view_results(election_id):
    """
    View the group assignment after clustering is done.
    """
    election = get_election_by_id(election_id)
    groups = get_groups_by_election(election_id)

    # Build a mapping: group ID → list of student objects
    group_data = []
    for group in groups:
        members = get_members_by_group(group.id)
        student_list = [Student.query.get(m.student_id) for m in members]
        group_data.append(student_list)

    return render_template('student/group_results.html',
                           election=election,
                           group_data=group_data)
