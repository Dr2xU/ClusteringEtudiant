from database.load_tables import load_all_data

data = load_all_data()

def parse_user():
    return data["users"]

def parse_election():
    return data["elections"]

def parse_teacher():
    teachers = [user for user in data["users"] if user[3] == "teacher"]
    return teachers

def parse_student():
    students = [user for user in data["users"] if user[3] == "student"]
    return students

def parse_election_participants(election_id):
    participants = [participant for participant in data["election_participants"] if participant[0] == election_id]
    return participants

def parse_group_members(group_id):
    members = [member for member in data["group_members"] if member[0] == group_id]
    return members

def parse_election_groups(election_id):
    groups = [group for group in data["election_groups"] if group[0] == election_id]
    return groups

def parse_student_votes(student_id):
    votes = [vote for vote in data["student_votes"] if vote[0] == student_id]
    return votes

def parse_election_votes(election_id):
    votes = [vote for vote in data["election_votes"] if vote[0] == election_id]
    return votes
