import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from app.extensions import db

class Group(db.Model):
    """
    Group model representing a student group generated from an election.
    Each group belongs to one election and contains multiple students.
    """

    __tablename__ = 'groups'

    # Unique group ID
    id = db.Column(db.Integer, primary_key=True)

    # Name of the group
    group_name = db.Column(db.String(100))
    
    # Foreign key to the election this group belongs to
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)

    # Relationship to the Election model
    election = db.relationship('Election', backref=db.backref('groups', lazy=True))

    def __repr__(self):
        """
        String representation of the group instance.
        """
        return f"<Group {self.id}: {self.group_name} - Election {self.election_id}>"


class GroupMember(db.Model):
    """
    Association model that links students to a group.
    This enables a many-to-many relationship between students and groups,
    where each student is only in one group per election.
    """

    __tablename__ = 'group_members'

    # Composite primary key (group_id + student_id)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)

    # Relationship to Group
    group = db.relationship('Group', backref=db.backref('members', cascade='all, delete-orphan'))

    # Relationship to Student
    student = db.relationship('Student', backref=db.backref('group_memberships', cascade='all, delete-orphan'))

    def __repr__(self):
        """
        String representation of the group membership instance.
        """
        return f"<GroupMember student={self.student_id} group={self.group_id}>"
