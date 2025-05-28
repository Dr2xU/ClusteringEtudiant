import sys
import os
import random
import string
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.models import Student, Election, StudentVote
from app.dao import add_student, add_or_update_vote, add_election
from app.services import list_elections_by_teacher
from app.extensions import db

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_dummy_students(num_students=15):
    """
    Generate dummy students with random attributes and save them to the DB.
    """
    for _ in range(num_students):
        unique_id = random_string(8)
        first_name = random_string(5).capitalize()
        last_name = random_string(7).capitalize()
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        class_name = f"Class {random.choice(['A', 'B', 'C', 'D'])}"
        section = random.choice(['1', '2', '3', '4'])
        password = "password"  # default password for dummy

        student = Student(
            unique_id=unique_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            class_name=class_name,
            section=section
        )
        student.set_password(password)
        add_student(student)
    db.session.commit()

def generate_dummy_election(teacher_id: int) -> Election:
    """
    Generate a dummy election for the given teacher_id with random data.
    Returns the created election instance.
    """
    title = f"Dummy Election {random.randint(1000, 9999)}"
    description = "This is a dummy election created for testing."
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=7)
    # students_per_group = random.choice([3, 4, 5])
    students_per_group = 3

    election = Election(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        students_per_group=students_per_group,
        teacher_id=teacher_id,
        status='running'
    )
    add_election(election)
    db.session.commit()

    # Associate all students to this election
    students = Student.query.all()
    election.students = students
    db.session.commit()

    return election

def generate_dummy_votes(election_id: int, student_ids: list[int], total_points: int = 100):
    """
    Generate dummy votes for each voter in student_ids.
    Each voter distributes total_points randomly among other students.
    """
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
    """
    Find all elections for a teacher and fill them with dummy votes for all students.
    """
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
    from app import create_app
    app = create_app()

    with app.app_context():
        teacher_id_input = input("Enter the teacher ID to fill all their elections with dummy votes: ")
        try:
            teacher_id = int(teacher_id_input)
        except ValueError:
            print("Invalid teacher ID. Must be an integer.")
            exit(1)

        print("Generating dummy students...")
        generate_dummy_students()

        print("Generating dummy election...")
        election = generate_dummy_election(teacher_id)

        print("Generating dummy votes...")
        students = Student.query.all()
        student_ids = [s.id for s in students]
        generate_dummy_votes(election.id, student_ids)

        print("Done.")
