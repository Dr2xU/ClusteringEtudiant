import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from datetime import datetime

# Association table for many-to-many between Election and Student
election_students = db.Table(
    'election_students',
    db.Column('election_id', db.Integer, db.ForeignKey('elections.id', ondelete='CASCADE'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), primary_key=True)
)

class Election(db.Model):
    """
    Election model representing a voting session or grouping event
    created by a teacher. Students vote during this election to express
    preferences for collaborators.
    """

    __tablename__ = 'elections'  # Name of the table in the database

    # Unique identifier for the election
    id = db.Column(db.Integer, primary_key=True)

    # Title or label for the election
    title = db.Column(db.String(100), nullable=False)

    # Optional description or purpose of the election
    description = db.Column(db.Text, nullable=True)

    # Start and end dates for when voting is allowed
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)

    # Maximum number of students allowed per group
    students_per_group = db.Column(db.Integer, nullable=False, default=3)

    # Foreign key to the teacher who created the election
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)

    # Relationship to the teacher (assuming Teacher model exists)
    teacher = db.relationship(
        'Teacher',
        backref=db.backref('elections', lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    )

    # Many-to-many relationship with students via association table
    students = db.relationship(
        'Student',
        secondary=election_students,
        back_populates='elections',
        lazy='subquery',
        passive_deletes=True
    )

    # Status of the election (e.g., running, paused, finished)
    status = db.Column(db.String(20), default='running')

    # Timestamp when the election was created
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """
        String representation for debugging purposes.
        """
        return f"<Election {self.title} by Teacher {self.teacher_id}>"
