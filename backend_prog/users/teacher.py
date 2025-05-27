from database.save_tables import save_election, save_election_participant, save_election_group
from elections.election import Election
from utils.parser import parse_election, parse_election_groups, parse_election_participants, parse_teacher, parse_student
class Teacher:
    
    def create_election(election_id, date_debut, date_fin, candidats, teacher_id):
        save_election(Election(election_id, date_debut, date_fin, candidats, teacher_id))

    def modify_election():
        pass

    def delete_election():
        pass

    def view_elections(teacher_id):
        elections = parse_election()
        teacher_elections = [election for election in elections if election.teacher_id == teacher_id]
        return teacher_elections
    
    def view_election_infos(election_id):
        elections = parse_election()
        for election in elections:
            if election.election_id == election_id:
                return election
        return None
    
    def add_student_to_election(election_id, student_id):
        save_election_participant(election_id, student_id)
        
    def stop_election(election_id):
        view_result_from_election(election_id)  
        
def view_result_from_election(election_id):
    groups = parse_election_groups(election_id)
    for group in groups:
        members = parse_election_participants(group.group_id)
        print(f"Group {group.group_id} members: {', '.join([member.student_id for member in members])}")
        
     

    def pause_election():
        pass
    
    def remove_student_from_election():
        pass

        
        

    

    