import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from datetime import datetime
from app import create_app
from app.extensions import db

from app.services.admin_service import create_admin, authenticate_admin
from app.services.teacher_service import create_teacher, authenticate_teacher
from app.services.student_service import create_student, authenticate_student
from app.services.election_service import (
    create_election,
    get_election_by_id,
    list_elections_by_teacher
)

def generate_unique_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def app():
    """
    Create a Flask test app with an in-memory SQLite database.
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
    return db.session

def test_admin_service(session):
    admin = create_admin("admin@test.com", "adminpass", "Alice", "Admin")
    assert admin.email == "admin@test.com"
    assert authenticate_admin("admin@test.com", "adminpass")
    assert not authenticate_admin("admin@test.com", "wrongpass")

import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from datetime import datetime
from app import create_app
from app.extensions import db

from app.services.admin_service import create_admin, authenticate_admin
from app.services.teacher_service import create_teacher, create_teacher_with_id, authenticate_teacher
from app.services.student_service import create_student_with_id, authenticate_student
from app.services.election_service import (
    create_election,
    get_election_by_id,
    list_elections_by_teacher
)

def generate_unique_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def app():
    """
    Create a Flask test app with an in-memory SQLite database.
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
    return db.session

def test_admin_service(session):
    admin = create_admin("admin@test.com", "adminpass", "Alice", "Admin")
    assert admin.email == "admin@test.com"
    assert authenticate_admin("admin@test.com", "adminpass")
    assert not authenticate_admin("admin@test.com", "wrongpass")

def test_teacher_service(session):
    unique_id = generate_unique_id("teacher")
    teacher = create_teacher_with_id(unique_id, "teacher@test.com", "teachpass", "Bob", "Teacher", "Physics")
    assert teacher.department == "Physics"
    assert authenticate_teacher("teacher@test.com", "teachpass")
    assert not authenticate_teacher("teacher@test.com", "wrongpass")

def test_student_service(session):
    unique_id = generate_unique_id("student")
    student = create_student_with_id(unique_id, "student@test.com", "studypass", "Charlie", "Student", "CS101", "A")
    assert student.class_name == "CS101"
    assert student.section == "A"
    assert authenticate_student("student@test.com", "studypass")
    assert not authenticate_student("student@test.com", "badpass")

def test_create_and_fetch_election(session):
    unique_id = generate_unique_id("teacher")
    teacher = create_teacher(unique_id, "teacher2@test.com", "pass", "Dana", "Doe", "Math")
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 10)

    election = create_election(
        title="Project Groups",
        start_date=start,
        end_date=end,
        teacher_id=teacher.id,
        students_per_group=2,
        description="Final project grouping"
    )

    assert election.title == "Project Groups"
    assert election.teacher_id == teacher.id

    fetched = get_election_by_id(election.id)
    assert fetched is not None
    assert fetched.description == "Final project grouping"

    elections_by_teacher = list_elections_by_teacher(teacher.id)
    assert len(elections_by_teacher) == 1


def test_create_and_fetch_election(session):
    unique_id = generate_unique_id("teacher")
    teacher = create_teacher(unique_id, "teacher2@test.com", "pass", "Dana", "Doe", "Math")
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 10)

    election = create_election(
        title="Project Groups",
        start_date=start,
        end_date=end,
        teacher_id=teacher.id,
        students_per_group=2,
        description="Final project grouping"
    )

    assert election.title == "Project Groups"
    assert election.teacher_id == teacher.id

    fetched = get_election_by_id(election.id)
    assert fetched is not None
    assert fetched.description == "Final project grouping"

    elections_by_teacher = list_elections_by_teacher(teacher.id)
    assert len(elections_by_teacher) == 1
