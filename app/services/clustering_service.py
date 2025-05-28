import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from sklearn.cluster import AgglomerativeClustering
import numpy as np
from app.models import StudentVote, Group, GroupMember
from app.extensions import db
from .openai_service import OpenAIService
from app.models import Student

def form_groups_from_votes(election_id: int, student_ids: list[int], group_size: int) -> tuple[dict, float]:
    """
    Clusters students into groups based on voting preferences and calculates group quality.

    Args:
        election_id (int): Election ID
        student_ids (list[int]): List of student IDs in the election
        group_size (int): Number of students per group

    Returns:
        tuple: (student_to_group dict, total_affinity_score float)
    """
    n_students = len(student_ids)
    if n_students < group_size:
        raise ValueError("Not enough students to form a group.")

    n_groups = max(1, n_students // group_size)
    index_map = {sid: i for i, sid in enumerate(student_ids)}
    reverse_map = {i: sid for sid, i in index_map.items()}

    affinity = np.zeros((n_students, n_students))
    votes = StudentVote.query.filter_by(election_id=election_id).all()

    # Populate affinity matrix
    for vote in votes:
        if vote.voter_id in index_map and vote.candidate_id in index_map:
            i = index_map[vote.voter_id]
            j = index_map[vote.candidate_id]
            affinity[i][j] += vote.score
            affinity[j][i] += vote.score  # Symmetric

    max_affinity = np.max(affinity) if np.max(affinity) > 0 else 1
    distance = max_affinity - affinity

    clustering = AgglomerativeClustering(
        n_clusters=n_groups,
        affinity='precomputed',
        linkage='average'
    )
    labels = clustering.fit_predict(distance)
    student_to_group = {reverse_map[i]: labels[i] for i in range(n_students)}

    # Score: sum of intra-group affinities
    total_score = 0
    for g in range(n_groups):
        group_members = [i for i, label in enumerate(labels) if label == g]
        for i in group_members:
            for j in group_members:
                if i != j:
                    total_score += affinity[i][j]

    # Normalize score (optional)
    total_score = total_score / 2  # each pair counted twice

    return student_to_group, total_score

def persist_groups(election_id: int, student_to_group: dict) -> None:
    """
    Persist the computed student groups to the database and generate group names.

    Args:
        election_id (int): Election ID
        student_to_group (dict): student_id → group_label mapping

    Returns:
        None
    """
    # Delete existing groups and members
    old_groups = Group.query.filter_by(election_id=election_id).all()
    for group in old_groups:
        GroupMember.query.filter_by(group_id=group.id).delete()
        db.session.delete(group)
    db.session.commit()

    group_label_to_group_obj = {}
    group_label_to_student_names = {}

    for student_id, group_label in student_to_group.items():
        if group_label not in group_label_to_group_obj:
            group = Group(election_id=election_id)
            db.session.add(group)
            db.session.flush()  # Get ID
            group_label_to_group_obj[group_label] = group
            group_label_to_student_names[group_label] = []

        group = group_label_to_group_obj[group_label]

        # Add student to the group member list
        db.session.add(GroupMember(group_id=group.id, student_id=student_id))

        # Collect first names for group naming
        student = Student.query.get(student_id)
        if student and student.first_name:
            group_label_to_student_names[group_label].append(student.first_name)

    db.session.flush()  # Ensure all GroupMember entries are saved before naming

    # Instantiate the OpenAI naming service
    group_namer = OpenAIService()

    # Generate and assign group names
    for group_label, group in group_label_to_group_obj.items():
        first_names = group_label_to_student_names.get(group_label, [])
        group_name = group_namer.generate_group_name_from_initials(first_names)
        group.group_name = group_name

    db.session.commit()
