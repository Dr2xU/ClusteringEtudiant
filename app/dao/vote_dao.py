import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import StudentVote

def add_or_update_vote(vote: StudentVote) -> StudentVote:
    """
    Adds a new vote or updates an existing vote in the database.

    Args:
        vote (StudentVote): The vote instance to save or update

    Returns:
        StudentVote: The saved vote
    """
    existing_vote = StudentVote.query.filter_by(
        election_id=vote.election_id,
        voter_id=vote.voter_id,
        candidate_id=vote.candidate_id
    ).first()

    if existing_vote:
        existing_vote.score = vote.score  # update score
    else:
        db.session.add(vote)  # new vote

    db.session.commit()
    return vote or existing_vote

def get_votes_by_voter(election_id: int, voter_id: int) -> list:
    """
    Get all votes cast by a specific student in an election.

    Args:
        election_id (int): Election ID
        voter_id (int): Voter's student ID

    Returns:
        list: List of StudentVote objects
    """
    return StudentVote.query.filter_by(
        election_id=election_id,
        voter_id=voter_id
    ).all()

def get_votes_for_candidate(election_id: int, candidate_id: int) -> list:
    """
    Get all votes received by a student in an election.

    Args:
        election_id (int): Election ID
        candidate_id (int): Candidate student ID

    Returns:
        list: List of StudentVote objects
    """
    return StudentVote.query.filter_by(
        election_id=election_id,
        candidate_id=candidate_id
    ).all()

def get_all_votes_for_election(election_id: int) -> list:
    """
    Get every vote cast in a specific election.

    Args:
        election_id (int): The election ID

    Returns:
        list: All StudentVote objects in the election
    """
    return StudentVote.query.filter_by(election_id=election_id).all()

def delete_votes_by_voter(election_id: int, voter_id: int) -> int:
    """
    Delete all votes cast by a student in an election.

    Args:
        election_id (int): Election ID
        voter_id (int): Student who cast the votes

    Returns:
        int: Number of deleted vote records
    """
    votes = get_votes_by_voter(election_id, voter_id)
    count = len(votes)
    for vote in votes:
        db.session.delete(vote)

    db.session.commit()
    return count
