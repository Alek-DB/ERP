from ERP_data_base import DatabaseManager
import sqlite3
class EmployeDAO:
    def __init__(self):
        self.db_manager = DatabaseManager()  
        
        
    def get_column_names(self):
        """Obtiene los nombres de las columnas de la tabla Employes."""
        query = "PRAGMA table_info(Employes);"
        columns_info = self.db_manager.execute_query(query)
        return [column[1] for column in columns_info]
    
    def search_employees(self, search_text):
        """Search employees by name, code, or other fields."""
        query = "SELECT * FROM Employes WHERE code_unique LIKE ? OR nom LIKE ? OR prenom LIKE ?"
        result = self.db_manager.execute_query(query, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        if result:
            column_names = [column[0] for column in self.db_manager.execute_query("PRAGMA table_info(Employes);")]
            return [dict(zip(column_names, row)) for row in result]
        return []


    def get_employe_by_id(self, id_employe):
            query = "SELECT * FROM Employes WHERE id_employe = ?"
            results = self.db_manager.execute_query(query, (id_employe,))
            if results:
                column_names = []
                try:
                    # Obtener los nombres de las columnas de la tabla 'Employes'
                    column_query = "PRAGMA table_info(Employes);"
                    columns_info = self.db_manager.execute_query(column_query)
                    
                    # Extraer solo los nombres de las columnas
                    column_names = [column[1] for column in columns_info]
                except sqlite3.Error as e:
                    print(f"Error al obtener información de la tabla: {e}")
                # Convertir las filas en diccionarios utilizando los nombres de las columnas
                return [dict(zip(column_names, row)) for row in results]
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