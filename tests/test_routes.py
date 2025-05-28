import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import pytest
from app import create_app
from app.extensions import db
from app.models import Admin, Teacher, Student

@pytest.fixture
def app():
    """
    Create a Flask app with in-memory database for testing routes.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seed_users():
    """
    Create a sample admin, teacher, and student in the DB.
    """
    admin = Admin(email="admin@test.com")
    admin.set_password("adminpass")

    teacher = Teacher(email="teacher@test.com")
    teacher.set_password("teachpass")

    student = Student(email="student@test.com")
    student.set_password("studypass")

    db.session.add_all([admin, teacher, student])
    db.session.commit()

    return {
        "admin": {"email": admin.email, "password": "adminpass"},
        "teacher": {"email": teacher.email, "password": "teachpass"},
        "student": {"email": student.email, "password": "studypass"}
    }

def login(client, email, password, role):
    """
    Helper to perform login.
    """
    return client.post('/auth/login', data={
        "email": email,
        "password": password,
        "role": role
    }, follow_redirects=True)

def test_login_logout(client, seed_users):
    res = login(client, **seed_users["admin"], role="admin")
    assert b"Logged in as admin" in res.data

    res = client.get('/auth/logout', follow_redirects=True)
    assert b"logged out" in res.data.lower()

def test_admin_dashboard_access(client, seed_users):
    login(client, **seed_users["admin"], role="admin")
    res = client.get('/admin/teachers')
    assert res.status_code == 200
    assert b"Teacher Management" in res.data

def test_teacher_dashboard_access(client, seed_users):
    login(client, **seed_users["teacher"], role="teacher")
    res = client.get('/teacher/')
    assert res.status_code == 200
    assert b"Your Elections" in res.data

def test_student_dashboard_access(client, seed_users):
    login(client, **seed_users["student"], role="student")
    res = client.get('/student/')
    assert res.status_code == 200
    assert b"Available Elections" in res.data or b"No elections" in res.data

def test_invalid_login(client):
    res = login(client, email="fake@user.com", password="wrong", role="admin")
    assert b"Invalid credentials" in res.data
