# Initialize the services package.
# This file can be used to expose or alias frequently-used service functions.

# Example: Direct imports for convenience
from .admin_service import (
    create_admin,
    get_admin_by_email,
    authenticate_admin,
    list_all_admins
)

from .teacher_service import (
    create_teacher,
    get_teacher_by_email,
    authenticate_teacher,
    list_all_teachers,
    delete_teacher,
    get_teacher_by_id,
    update_teacher_profile,
    update_teacher_password
)

from .student_service import (
    create_student,
    get_student_by_email,
    authenticate_student,
    list_all_students,
    delete_student,
    get_student_by_id,
    update_student_profile,
    update_student_password
)

from .election_service import (
    create_election,
    get_election_by_id,
    list_elections_by_teacher,
    update_election_status,
    delete_election
)

from .vote_service import (
    cast_vote,
    get_votes_by_student,
    get_votes_for_candidate,
    get_all_votes_for_election,
    delete_votes_by_student
)

from .clustering_service import (
    form_groups_from_votes,
    persist_groups
)

from .openai_service import OpenAIService
