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
    
     # Méthodes pour modifier chaque attribut
    def modifier_prenom(self, prenom):
        self.prenom = prenom

    def modifier_nom(self, nom):
        self.nom = nom

    def modifier_poste(self, poste):
        self.poste = poste

    def modifier_salaire(self, salaire):
        self.salaire = salaire

    def modifier_date_naissance(self, date_naissance):
        self.date_naissance = date_naissance

    def modifier_date_embauche(self, date_embauche):
        self.date_embauche = date_embauche

    def modifier_sexe(self, sexe):
        self.sexe = sexe

    def modifier_statut(self, statut):
        self.statut = statut

    def modifier_allergies_preferences(self, allergies_preferences):
        self.allergies_preferences_alimentaires = allergies_preferences

    def modifier_code_unique(self, code_unique):
        self.code_unique = code_unique

    def modifier_role(self, role):
        self.role = role  # Méthode pour modifier le rôle

    def add_to_db(self):
        dao = EmployeDAO()
        role_str = Role.get_role_name(self.role)
        return dao.add_employe(self)
