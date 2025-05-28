# Initialize the DAO (Data Access Object) package.
# This file aggregates commonly used DAO functions for easier imports.

from .admin_dao import (
    add_admin,
    get_admin_by_id,
    get_admin_by_email,
    list_all_admins,
    delete_admin
)

from .teacher_dao import (
    add_teacher,
    get_teacher_by_id,
    get_teacher_by_email,
    list_all_teachers,
    delete_teacher_by_id,
    update_teacher,
    update_teacher_password
)

from .student_dao import (
    add_student,
    get_student_by_id,
    get_student_by_email,
    list_all_students,
    delete_student_by_id,
    update_student,
    update_student_password
)

from .election_dao import (
    add_election,
    get_election_by_id,
    list_elections_by_teacher,
    update_election_status,
    delete_election
)

from .vote_dao import (
    add_or_update_vote,
    get_votes_by_voter,
    get_votes_for_candidate,
    get_all_votes_for_election,
    delete_votes_by_voter
)

from .group_dao import (
    add_group,
    add_group_member,
    get_groups_by_election,
    get_members_by_group,
    delete_groups_by_election
)
