class Election:
    
    def __init__(self, id_election, date_debut, date_fin, candidats, id_teacher):
        self.id_election = id_election
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.candidats = candidats
        self.id_teacher = id_teacher

    def __str__(self):
        return f"Election(id_election={self.id_election}, date_debut={self.date_debut}, date_fin={self.date_fin}, id_candidat={self.id_teacher}, candidats={self.candidats})"
    
