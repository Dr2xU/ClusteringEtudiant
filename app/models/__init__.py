# This file aggregates all model definitions for easy access and registration.

# Import each model class to ensure SQLAlchemy can detect and create the tables.

from app.models.admin import Admin         # Admin user model
from app.models.teacher import Teacher     # Teacher user model
from app.models.student import Student     # Student user model
from app.models.election import Election   # Election model created by teachers
from app.models.vote import StudentVote    # Voting record between students
from app.models.group import Group, GroupMember  # Group and group membership models