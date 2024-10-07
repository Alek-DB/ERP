from ERP_data_base import DatabaseManager

class EmployeDAO:
    def __init__(self):
        self.db_manager = DatabaseManager()  # Get the singleton instance

    def add_employe(self, employe):
        query = """
        INSERT INTO Employes (nom, prenom, poste, salaire, date_naissance, date_embauche, sexe, statut, allergies_preferences_alimentaires, code_unique)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            employe.nom,
            employe.prenom,
            employe.poste,
            employe.salaire,
            employe.date_naissance,
            employe.date_embauche,
            employe.sexe,
            employe.statut,
            employe.allergies,
            employe.code_unique
        )
        rows_affected = self.db_manager.execute_update(query, parameters)
        return rows_affected > 0  # Return True if the insert was successful
