from database.save_tables import save_user
from utils.parser import parse_user, parse_teacher, parse_student, parse_election_participants, parse_group_members, parse_election_groups, parse_student_votes, parse_election_votes

class Admin():
    def add_user(id, email, password, role):
        save_user(id, email, password, role)

    def modify_user():
        pass

    def delete_user():
        pass

    def view_users():
        users = parse_user()
        return users

    def view_students():
        students = parse_student()
        return students

    def view_teachers():
        teachers = parse_teacher()
        return teachers
    
