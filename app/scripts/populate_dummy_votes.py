import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app  # Import your Flask app factory or app instance
from app.extensions import db
from app.services import list_elections_by_teacher
from app.models import Student
from app.dao.vote_dao import add_or_update_vote

import random

app = create_app()  # or import your app directly if not using factory

from app.models import StudentVote

def generate_dummy_votes(election_id: int, student_ids: list[int], total_points: int = 100):
    for voter_id in student_ids:
        candidates = [sid for sid in student_ids if sid != voter_id]
        if not candidates:
            continue
        remaining_points = total_points
        scores = {}
        remaining_candidates = len(candidates)
        for candidate_id in candidates:
            if remaining_candidates == 1:
                scores[candidate_id] = remaining_points
            else:
                max_alloc = remaining_points - (remaining_candidates - 1)
                score = random.randint(0, max_alloc)
                scores[candidate_id] = score
                remaining_points -= score
            remaining_candidates -= 1
        for candidate_id, score in scores.items():
            if score > 0:
                vote = StudentVote(
                    election_id=election_id,
                    voter_id=voter_id,
                    candidate_id=candidate_id,
                    score=score
                )
                add_or_update_vote(vote)
    db.session.commit()


def fill_teacher_elections_with_dummy_votes(teacher_id: int):
    elections = list_elections_by_teacher(teacher_id)
    if not elections:
        print(f"No elections found for teacher id {teacher_id}.")
        return

    students = Student.query.all()
    student_ids = [s.id for s in students]

    for election in elections:
        print(f"Filling election '{election.title}' (ID: {election.id}) with dummy votes...")
        generate_dummy_votes(election.id, student_ids)

if __name__ == '__main__':
    with app.app_context():
        teacher_id_input = input("Enter the teacher ID to fill all their elections with dummy votes: ")
        try:
            teacher_id = int(teacher_id_input)
        except ValueError:
            print("Invalid teacher ID. Must be an integer.")
            exit(1)
        fill_teacher_elections_with_dummy_votes(teacher_id)
        print("Done.")
