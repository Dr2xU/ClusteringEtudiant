import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from app.services.clustering_service import form_groups_from_votes
from app.models import StudentVote
from app.extensions import db
from app import create_app
import random

@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
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
def client(app):
    return app.test_client()

@pytest.fixture
def seed_votes(app):
    """
    Seed dummy student votes for a clustering test.
    """
    from app.models import Student, Election

    students = []
    for i in range(6):
        s = Student(email=f"student{i}@mail.com")
        s.set_password("pass")
        db.session.add(s)
        students.append(s)

    db.session.commit()

    election = Election(
        title="Mock Election",
        start_date="2024-01-01",
        end_date="2024-12-31",
        max_votes_per_student=3,
        students_per_group=2,
        teacher_id=1
    )
    db.session.add(election)
    db.session.commit()

    # Cast votes: each student randomly prefers 3 others
    for voter in students:
        choices = random.sample([s for s in students if s != voter], 3)
        for rank, candidate in enumerate(choices):
            vote = StudentVote(
                election_id=election.id,
                voter_id=voter.id,
                candidate_id=candidate.id,
                score=3 - rank  # 3, 2, 1
            )
            db.session.add(vote)

    db.session.commit()

    return election.id, [s.id for s in students]

def test_clustering_groups(app, seed_votes):
    """
    Ensure the clustering groups students into expected number of groups.
    """
    election_id, student_ids = seed_votes
    group_size = 2
    result, score = form_groups_from_votes(election_id, student_ids, group_size)

    assert isinstance(result, dict)
    assert len(result) == len(student_ids)
    group_labels = set(result.values())

    # Check number of groups is as expected
    expected_groups = len(student_ids) // group_size
    assert len(group_labels) == expected_groups
    assert score > 0
