import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import StudentVote

def cast_vote(election_id: int, voter_id: int, candidate_id: int, score: int) -> StudentVote:
    """
    Records a student's vote for a classmate in a specific election.
    If a vote already exists between the same voter and candidate in the same election, it updates the score.

    Args:
        election_id (int): ID of the election
        voter_id (int): ID of the student casting the vote
        candidate_id (int): ID of the student being voted for
        score (int): Affinity score (e.g., 3 = high preference, 0 = avoid)

    Returns:
        StudentVote: The newly created or updated vote record
    """
    vote = StudentVote.query.filter_by(
        election_id=election_id,
        voter_id=voter_id,
        candidate_id=candidate_id
    ).first()

    if vote:
        vote.score = score  # update existing vote
    else:
        vote = StudentVote(
            election_id=election_id,
            voter_id=voter_id,
            candidate_id=candidate_id,
            score=score
        )
        db.session.add(vote)

    db.session.commit()
    return vote

def get_votes_by_student(election_id: int, voter_id: int) -> list:
    """
    Retrieve all votes cast by a specific student in an election.

    Args:
        election_id (int): The election ID
        voter_id (int): The voter's student ID

    Returns:
        list: List of StudentVote objects
    """
    return StudentVote.query.filter_by(
        election_id=election_id,
        voter_id=voter_id
    ).all()

def get_votes_for_candidate(election_id: int, candidate_id: int) -> list:
    """
    Get all votes received by a specific candidate in a given election.

    Args:
        election_id (int): The election ID
        candidate_id (int): The candidate's student ID

    Returns:
        list: List of StudentVote objects
    """
    return StudentVote.query.filter_by(
        election_id=election_id,
        candidate_id=candidate_id
    ).all()

def get_all_votes_for_election(election_id: int) -> list:
    """
    Retrieve all votes cast in an election.

    Args:
        election_id (int): The election ID

    Returns:
        list: List of all StudentVote objects in that election
    """
    return StudentVote.query.filter_by(election_id=election_id).all()

def delete_votes_by_student(election_id: int, voter_id: int) -> int:
    """
    Deletes all votes cast by a student in a given election.

    Args:
        election_id (int): The election ID
        voter_id (int): The voter's student ID

    Returns:
        int: Number of deleted vote records
    """
    votes = StudentVote.query.filter_by(
        election_id=election_id,
        voter_id=voter_id
    ).all()

    count = len(votes)
    for vote in votes:
        db.session.delete(vote)

    db.session.commit()
    return count