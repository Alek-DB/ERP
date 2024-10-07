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
