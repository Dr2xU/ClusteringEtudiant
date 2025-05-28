import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import (
    get_all_votes_for_election,
    cast_vote,
    delete_votes_by_student,
    get_votes_by_student,
    get_election_by_id,
    get_student_by_id,
    update_student_profile,
    update_student_password
)
from app.models import Student, StudentVote
from app.dao import get_groups_by_election, get_members_by_group
from functools import wraps

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'student':
            flash("You must be logged in as a student to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/')
@student_required
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
    return render_template('student/dashboard.html', elections=elections, student=student)

@student_bp.route('/complete-profile', methods=['GET', 'POST'])
@student_required
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
@student_required
def vote(election_id):
    student_id = session.get('user_id')
    election = get_election_by_id(election_id)

    if election.status == 'finished':
        flash("Voting for this election is closed.", "warning")
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        raw_scores = request.form.to_dict(flat=False)

        scores = {}
        total_score = 0
        for key, value in raw_scores.items():
            if key.startswith('scores[') and key.endswith(']'):
                try:
                    student_key = int(key[7:-1])
                    score_val = int(value[0]) if value else 0
                    if score_val < 0:
                        score_val = 0  # Ensure no negative scores
                    scores[student_key] = score_val
                    total_score += score_val
                except ValueError:
                    continue

        # Validate total score does not exceed 100
        if total_score > 100:
            flash(f"Total score cannot exceed 100. You have assigned {total_score}.", "danger")
        else:
            delete_votes_by_student(election_id, student_id)
            for candidate_id, score in scores.items():
                if score > 0:
                    cast_vote(election_id, student_id, candidate_id, score)
            flash("Votes submitted successfully.", "success")
            return redirect(url_for('student.dashboard'))

        # If validation failed, re-render form with existing votes
        students = election.students
        existing_votes = get_votes_by_student(election_id, student_id)
        voted_ids = {vote.candidate_id: vote.score for vote in existing_votes}
        return render_template('student/vote_form.html', election=election, students=students, voted_ids=voted_ids)

    # GET method: show vote form with previous votes filled
    students = election.students
    existing_votes = get_votes_by_student(election_id, student_id)
    voted_ids = {vote.candidate_id: vote.score for vote in existing_votes}

    return render_template('student/vote_form.html', election=election, students=students, voted_ids=voted_ids)



@student_bp.route('/election/<int:election_id>/results')
@student_required
def view_results(election_id):
    election = get_election_by_id(election_id)
    groups = get_groups_by_election(election_id)

    # Get all votes for this election (list of StudentVote)
    votes = StudentVote.query.filter_by(election_id=election_id).all()

    # Build a mapping: voter_id -> dict of candidate_id -> score
    votes_map = {}
    for vote in votes:
        votes_map.setdefault(vote.voter_id, {})[vote.candidate_id] = vote.score

    # Build group data with members and their votes
    group_data = []
    for group in groups:
        members = get_members_by_group(group.id)
        students = [Student.query.get(m.student_id) for m in members]
        group_data.append({
            'group': group,
            'members': students,
        })

    return render_template('student/group_results.html',
                           election=election,
                           group_data=group_data,
                           votes_map=votes_map)

