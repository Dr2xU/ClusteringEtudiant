import sys
import os
import random
import datetime
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services import run_full_grouping
from app.models import StudentVote
from app.extensions import db
from app import create_app


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ECHO": False,
    })

    with app.app_context():
        # Drop all tables first to avoid "table exists" errors
        db.drop_all()
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
        s = Student(
            unique_id=f"student{i:03d}",
            email=f"student{i}@mail.com"
        )
        s.set_password("pass")
        db.session.add(s)
        students.append(s)

    db.session.commit()

    election = Election(
        title="Mock Election",
        start_date=datetime.date(2024, 1, 1),
        end_date=datetime.date(2024, 12, 31),
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
                score=3 - rank  # scores 3, 2, 1
            )
            db.session.add(vote)

    db.session.commit()

    return election.id, [s.id for s in students]


def test_clustering_groups(app, seed_votes):
    election_id, student_ids = seed_votes
    group_size = 2

    # run_full_grouping returns: student_to_group, global_score, groups_to_highlight, total_satisfaction, avg_satisfaction
    student_to_group, score, highlights, total_satisfaction, avg_satisfaction = run_full_grouping(election_id, student_ids, group_size)

    assert isinstance(student_to_group, dict)
    assert len(student_to_group) == len(student_ids)

    group_labels = set(student_to_group.values())
    expected_groups = len(student_ids) // group_size
    assert len(group_labels) >= expected_groups
    assert score > 0

    assert total_satisfaction >= 0
    assert 0 <= avg_satisfaction <= total_satisfaction
