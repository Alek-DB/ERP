from employe.ERP_employeDAO import EmployeDAO
from ERP_role import Role

class Employe:
    def __init__(self, prenom, nom, poste, salaire, date_naissance, date_embauche, sexe, statut, allergies, code_unique, role):
        self.prenom = prenom
        self.nom = nom
        self.poste = poste
        self.salaire = salaire
        self.date_naissance = date_naissance
        self.date_embauche = date_embauche
        self.sexe = sexe
        self.statut = statut
        self.allergies = allergies
        self.code_unique = code_unique
        self.role = role

    def add_to_db(self):
        dao = EmployeDAO()
        role_str = Role.get_role_name(self.role)
        return dao.add_employe(self)
