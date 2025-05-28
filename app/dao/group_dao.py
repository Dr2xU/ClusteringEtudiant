import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from app.extensions import db
from app.models import Group, GroupMember

def add_group(group: Group) -> Group:
    """
    Adds a new Group to the database.

    Args:
        group (Group): The group instance to persist

    Returns:
        Group: The saved Group object
    """
    db.session.add(group)
    db.session.flush()  # Ensures group.id is available before committing
    return group

def add_group_member(group_id: int, student_id: int) -> GroupMember:
    """
    Adds a student to a group as a GroupMember.

    Args:
        group_id (int): ID of the group
        student_id (int): ID of the student

    Returns:
        GroupMember: The persisted GroupMember object
    """
    membership = GroupMember(group_id=group_id, student_id=student_id)
    db.session.add(membership)
    db.session.commit()
    return membership

def get_groups_by_election(election_id: int) -> list:
    """
    Retrieve all groups formed during a given election.

    Args:
        election_id (int): The election ID

    Returns:
        list: List of Group objects
    """
    return Group.query.filter_by(election_id=election_id).all()

def get_members_by_group(group_id: int) -> list:
    """
    Get all students in a specific group.

    Args:
        group_id (int): ID of the group

    Returns:
        list: List of GroupMember objects
    """
    return GroupMember.query.filter_by(group_id=group_id).all()

def delete_groups_by_election(election_id: int) -> int:
    """
    Delete all groups and their members from a given election.

    Args:
        election_id (int): Election ID to clear

    Returns:
        int: Number of deleted group records
    """
    groups = get_groups_by_election(election_id)
    deleted_count = 0
    for group in groups:
        GroupMember.query.filter_by(group_id=group.id).delete()
        db.session.delete(group)
        deleted_count += 1
    db.session.commit()
    return deleted_count
