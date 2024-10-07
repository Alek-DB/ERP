class EmployeDAO:
    def __init__(self, db_path='erp_database.db'):
        self.db_manager = DatabaseManager(db_path)

    def get_employe_by_id(self, id_employe):
        query = "SELECT * FROM Employes WHERE id_employe = ?"
        results = self.db_manager.execute_query(query, (id_employe,))
        if results:
            return results[0]  # Retourne le premier enregistrement trouvé
        else:
            return None

    def add_employe(self, employe_data):
        query = """
        INSERT INTO Employes (nom, prenom, poste, salaire, date_naissance, date_embauche, sexe, statut,
                              allergies_preferences_alimentaires, code_unique, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            employe_data['nom'],
            employe_data['prenom'],
            employe_data['poste'],
            employe_data['salaire'],
            employe_data['date_naissance'],
            employe_data['date_embauche'],
            employe_data['sexe'],
            employe_data['statut'],
            employe_data['allergies_preferences_alimentaires'],
            employe_data['code_unique'],
            employe_data['role']  # Include the role in the parameters
        )
        rows_affected = self.db_manager.execute_update(query, parameters)
        return rows_affected > 0

    def update_employe(self, employe_data):
        query = """
        UPDATE Employes SET nom = ?, prenom = ?, poste = ?, salaire = ?, date_naissance = ?, 
        date_embauche = ?, sexe = ?, statut = ?, allergies_preferences_alimentaires = ?, 
        code_unique = ?, role = ? WHERE id_employe = ?
        """
        parameters = (
            employe_data['nom'],
            employe_data['prenom'],
            employe_data['poste'],
            employe_data['salaire'],
            employe_data['date_naissance'],
            employe_data['date_embauche'],
            employe_data['sexe'],
            employe_data['statut'],
            employe_data['allergies_preferences_alimentaires'],
            employe_data['code_unique'],
            employe_data['role'],  # Include the role in the parameters
            employe_data['id_employe']  # Ensure the ID is also passed for the update
        )
        rows_affected = self.db_manager.execute_update(query, parameters)
        return rows_affected > 0

    def delete_employe(self, id_employe):
        query = "DELETE FROM Employes WHERE id_employe = ?"
        rows_affected = self.db_manager.execute_update(query, (id_employe,))
        return rows_affected > 0
