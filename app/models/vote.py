import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db

class StudentVote(db.Model):
    """
    StudentVote model represents a student's preference for another student
    during a specific election. Votes contribute to affinity scoring for clustering.
    """

    __tablename__ = 'student_votes'

    # Unique identifier for each vote entry
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key to the election this vote belongs to
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id', ondelete='CASCADE'), nullable=False)

    # Foreign key to the student who casts the vote
    voter_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    # Foreign key to the student who is being voted for
    candidate_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    # Score assigned to the candidate (e.g., 3 for top choice, 1 for neutral, 0 for avoid)
    score = db.Column(db.Integer, nullable=False)

    # Timestamp of when the vote was cast
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships for ORM navigation
    election = db.relationship(
        'Election',
        backref=db.backref('votes', lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    )
    voter = db.relationship(
        'Student',
        foreign_keys=[voter_id],
        backref=db.backref('votes_cast', lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    )
    candidate = db.relationship(
        'Student',
        foreign_keys=[candidate_id],
        backref=db.backref('votes_received', lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    )

    def __repr__(self):
        """
        Debugging representation of a single vote.
        """
        return f"<Vote voter={self.voter_id} → candidate={self.candidate_id} | score={self.score}>"
