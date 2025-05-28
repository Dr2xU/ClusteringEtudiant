import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from app import create_app
from app.extensions import db
from app.models import Admin, Teacher, Student, Election, StudentVote

@pytest.fixture
def app():
    """
    Create a Flask app with an in-memory test database.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    """
    Provide a clean database session for each test.
    """
    with app.app_context():
        yield db.session

def test_admin_creation_and_auth(session):
    admin = Admin(email="admin@test.com")
    admin.set_password("securepass")

    session.add(admin)
    session.commit()

    loaded = Admin.query.filter_by(email="admin@test.com").first()
    assert loaded is not None
    assert loaded.check_password("securepass")
    assert not loaded.check_password("wrongpass")

def test_teacher_model(session):
    teacher = Teacher(email="teacher@test.com", first_name="Jane", department="Math")
    teacher.set_password("teachpass")
    session.add(teacher)
    session.commit()

    found = Teacher.query.filter_by(email="teacher@test.com").first()
    assert found is not None
    assert found.first_name == "Jane"
    assert found.check_password("teachpass")

def test_student_model(session):
    student = Student(email="student@test.com", class_name="CS101", section="A")
    student.set_password("studypass")
    session.add(student)
    session.commit()

    found = Student.query.filter_by(email="student@test.com").first()
    assert found is not None
    assert found.class_name == "CS101"
    assert found.section == "A"
    assert found.check_password("studypass")

def test_election_creation(session):
    teacher = Teacher(email="owner@test.com")
    teacher.set_password("pass")
    session.add(teacher)
    session.commit()

    election = Election(
        title="Group Election",
        start_date="2025-01-01",
        end_date="2025-01-10",
        teacher_id=teacher.id,
        max_votes_per_student=3,
        students_per_group=2
    )
    session.add(election)
    session.commit()

    assert Election.query.count() == 1
    assert election.title == "Group Election"

def test_student_vote_model(session):
    # Setup students and election
    s1 = Student(email="voter@test.com"); s1.set_password("123")
    s2 = Student(email="target@test.com"); s2.set_password("456")
    t = Teacher(email="t@e.com"); t.set_password("t")
    session.add_all([s1, s2, t]); session.commit()

    election = Election(
        title="Voting Test",
        start_date="2025-01-01",
        end_date="2025-01-10",
        teacher_id=t.id,
        max_votes_per_student=3,
        students_per_group=2
    )
    session.add(election)
    session.commit()

    vote = StudentVote(
        election_id=election.id,
        voter_id=s1.id,
        candidate_id=s2.id,
        score=3
    )
    session.add(vote)
    session.commit()

    fetched = StudentVote.query.filter_by(voter_id=s1.id).first()
    assert fetched is not None
    assert fetched.score == 3
