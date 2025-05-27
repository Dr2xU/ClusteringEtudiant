from database.save_tables import save_election_vote, save_student_vote
from utils.parser import parse_election
from elections.vote import Vote

class Student:
    
    def add_vote(Vote):
        save_election_vote(Vote["election_id"], Vote["id"])
        save_student_vote(Vote)

    def view_election_infos(election_id):
        elections = parse_election()
        for election in elections:
            if election.election_id == election_id:
                return election
        return None

    def view_result_from_election():
        pass

    def view_votes():
        pass
   
   
    def modify_vote():
        pass

    def delete_vote():
        pass

    
    