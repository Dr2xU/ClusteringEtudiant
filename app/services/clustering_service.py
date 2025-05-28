import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

from app.models import StudentVote, Group, GroupMember, Student
from app.extensions import db
from .openai_service import OpenAIService


def votes_for_student(election_id: int, student_ids: list[int]) -> dict[int, dict[int, int]]:
    """
    Get votes for each student in the election.
    Returns: dict student_id -> {candidate_id -> score}
    """
    votes = StudentVote.query.filter_by(election_id=election_id).all()
    vote_map = {sid: {} for sid in student_ids}

    for vote in votes:
        if vote.voter_id in vote_map and vote.candidate_id in student_ids:
            vote_map[vote.voter_id][vote.candidate_id] = vote.score

    return vote_map


def get_preferences(election_id: int, vote_map: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:
    """
    Prepare symmetric preference scores; multiply by 1.5 only if mutual vote exists.
    Fill missing votes with 0.
    """
    students = list(vote_map.keys())
    score_map = {}

    for sid in students:
        score_map[sid] = {}
        for cid in students:
            if cid in vote_map[sid]:
                # Mutual vote check
                if cid in vote_map and sid in vote_map[cid]:
                    score_map[sid][cid] = vote_map[sid][cid] * 1.5
                else:
                    score_map[sid][cid] = vote_map[sid][cid]
            else:
                score_map[sid][cid] = 0
    return score_map


def run_k_means(election_id: int, student_ids: list[int], group_size: int):
    """
    Run KMeans clustering on affinity matrix derived from votes.

    Returns:
        result_groups (list[list[int]]): student ID groups
        global_score (float): affinity score
    """
    vote_map = votes_for_student(election_id, student_ids)
    score_map = get_preferences(election_id, vote_map)

    n = len(student_ids)
    index_map = {sid: i for i, sid in enumerate(student_ids)}
    reverse_map = {i: sid for sid, i in index_map.items()}

    nb_groups = max(1, n // group_size)
    if n % group_size > 0:
        nb_groups += 1

    affinities = np.zeros((n, n))
    for sid, prefs in score_map.items():
        i = index_map[sid]
        for cid, score in prefs.items():
            j = index_map[cid]
            affinities[i][j] = score

    affinities = (affinities + affinities.T) / 2  # symmetric

    best_score = -float('inf')
    best_labels = None

    for seed in range(5):
        kmeans = KMeans(n_clusters=nb_groups, random_state=42 + seed, n_init=5)
        labels = kmeans.fit_predict(affinities)

        score = 0
        groups = [[] for _ in range(nb_groups)]
        for idx, lbl in enumerate(labels):
            groups[lbl].append(idx)

        for g in groups:
            for i in range(len(g)):
                for j in range(i + 1, len(g)):
                    score += affinities[g[i]][g[j]]

        if score > best_score:
            best_score = score
            best_labels = labels

    # Construct groups from best_labels
    groups = [[] for _ in range(nb_groups)]
    for idx, lbl in enumerate(best_labels):
        groups[lbl].append(idx)

    # --- REBALANCE STEP TO RESPECT group_size LIMIT ---
    groupes_trop_grands = [i for i, g in enumerate(groups) if len(g) > group_size]
    groupes_trop_petits = [i for i, g in enumerate(groups) if len(g) < group_size]

    while groupes_trop_grands and groupes_trop_petits:
        grand_idx = groupes_trop_grands[0]
        petit_idx = groupes_trop_petits[0]

        # Find the student to move minimizing affinity loss
        meilleur_etudiant = None
        min_perte = float('inf')

        for etud in groups[grand_idx]:
            perte_ancien = sum(affinities[etud][autre] for autre in groups[grand_idx] if autre != etud)
            gain_nouveau = sum(affinities[etud][autre] for autre in groups[petit_idx])
            perte_nette = perte_ancien - gain_nouveau
            if perte_nette < min_perte:
                min_perte = perte_nette
                meilleur_etudiant = etud

        # Move the student
        groups[grand_idx].remove(meilleur_etudiant)
        groups[petit_idx].append(meilleur_etudiant)

        # Update lists of too big/small groups
        if len(groups[grand_idx]) <= group_size:
            groupes_trop_grands.pop(0)
        if len(groups[petit_idx]) >= group_size:
            groupes_trop_petits.pop(0)

    # Map back to student IDs
    result_groups = []
    for g in groups:
        result_groups.append([reverse_map[idx] for idx in g])

    return result_groups, best_score



def create_groups_and_name(election_id: int, result_groups: list[list[int]]):
    """
    Persist groups and generate names using OpenAI.
    If OpenAIService is unavailable, fallback to concatenating
    first letters of first names capitalized.

    Args:
        election_id: int
        result_groups: List of student ID groups
    """
    # Delete old groups and members first
    old_groups = Group.query.filter_by(election_id=election_id).all()
    for group in old_groups:
        GroupMember.query.filter_by(group_id=group.id).delete()
        db.session.delete(group)
    db.session.commit()

    try:
        group_namer = OpenAIService()
        # Optionally verify API connectivity or key here
        api_available = True
    except Exception:
        group_namer = None
        api_available = False

    for group_members in result_groups:
        if not group_members:
            continue

        group = Group(election_id=election_id)
        db.session.add(group)
        db.session.flush()  # get group.id

        for student_id in group_members:
            db.session.add(GroupMember(group_id=group.id, student_id=student_id))

        # Generate group name from first names
        first_names = [Student.query.get(sid).first_name for sid in group_members if Student.query.get(sid) and Student.query.get(sid).first_name]

        if api_available and group_namer:
            try:
                group_name = group_namer.generate_group_name_from_initials(first_names)
            except Exception:
                group_name = ''.join(fn[0].upper() for fn in first_names if fn)
        else:
            group_name = ''.join(fn[0].upper() for fn in first_names if fn)

        group.group_name = group_name

    db.session.commit()


def groups_with_votes_between_members(election_id: int, student_to_group: dict[int, int]) -> set[int]:
    """
    Identify groups where at least one member voted for another member.

    Args:
        election_id: int
        student_to_group: Mapping student_id -> group_label (group.id)

    Returns:
        Set of group ids that should be highlighted
    """
    votes = StudentVote.query.filter_by(election_id=election_id).all()
    group_to_students = defaultdict(set)
    for student_id, group_label in student_to_group.items():
        group_to_students[group_label].add(student_id)

    highlight_groups = set()
    for vote in votes:
        voter_group = student_to_group.get(vote.voter_id)
        candidate_group = student_to_group.get(vote.candidate_id)
        if voter_group is not None and candidate_group is not None:
            if voter_group == candidate_group and vote.score > 0:
                highlight_groups.add(voter_group)
    return highlight_groups


def student_to_groups(student_to_group: dict[int, int]) -> list[list[int]]:
    groups = defaultdict(list)
    for student_id, group_id in student_to_group.items():
        groups[group_id].append(student_id)
    return list(groups.values())


def run_full_grouping(election_id: int, student_ids: list[int], group_size: int):
    """
    Full workflow: cluster, persist, generate names, and identify highlight groups.

    Returns:
        tuple: (student_to_group mapping, global_score, groups_to_highlight set)
    """
    # Run clustering (K-means) to get list of groups and score
    result_groups, global_score = run_k_means(election_id, student_ids, group_size)

    # Convert result_groups (list of lists) to student_to_group dict (student_id -> group_id)
    student_to_group = {}
    for group_id, group_members in enumerate(result_groups):
        for student_id in group_members:
            student_to_group[student_id] = group_id

    # Convert back to list of groups for persisting and naming
    groups_for_persist = student_to_groups(student_to_group)
    create_groups_and_name(election_id, groups_for_persist)

    # After persisting, re-fetch groups and map student_id to real group.id in DB
    groups = Group.query.filter_by(election_id=election_id).all()
    real_student_to_group = {}
    for group in groups:
        members = GroupMember.query.filter_by(group_id=group.id).all()
        for m in members:
            real_student_to_group[m.student_id] = group.id

    # Fetch vote map for satisfiability
    vote_map = votes_for_student(election_id, student_ids)

    # Calculate satisfiability score
    total_satisfaction, avg_satisfaction = calculate_satisfiability(real_student_to_group, vote_map)

    # Determine which groups to highlight based on voting relations
    groups_to_highlight = groups_with_votes_between_members(election_id, real_student_to_group)

    return real_student_to_group, global_score, groups_to_highlight, total_satisfaction, avg_satisfaction

def calculate_satisfiability(student_to_group: dict[int, int], vote_map: dict[int, dict[int, int]]):
    total_satisfaction = 0
    count_students = len(student_to_group)

    for student_id, group_id in student_to_group.items():
        votes = vote_map.get(student_id, {})
        group_mates = {sid for sid, gid in student_to_group.items() if gid == group_id and sid != student_id}

        satisfaction = sum(score for cid, score in votes.items() if cid in group_mates)
        total_satisfaction += satisfaction

    avg_satisfaction_per_student = total_satisfaction / count_students if count_students else 0
    return total_satisfaction, avg_satisfaction_per_student
