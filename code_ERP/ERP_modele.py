import requests
from ERP_data_base import DatabaseManager
import hashlib

class Modele:
    def __init__(self,db_manager):
        self.authenticated = False
        self.db_manager = db_manager

    def verifier_identifiants(self, username, password):
        # Simule une requête au serveur pour vérifier les identifiants
        try:
            response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200 and response.json().get('success'):
                return self.verifier_login(username,password)
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return False
           
    def verifier_login(self, username, mot_de_passe):
        # Exécuter la requête pour obtenir le mot de passe haché
        resultat = self.db_manager.execute_query("SELECT mot_de_passe FROM Employes WHERE username = ?", (username,))
        
        # Si un employé a été trouvé
        if resultat:
            mot_de_passe_hache = resultat[0][0]
            # Comparer le mot de passe fourni avec le mot de passe haché
            if mot_de_passe_hache == self.hacher_mot_de_passe(mot_de_passe):
                return "good"
            elif mot_de_passe_hache is None:
                return "first"
            else:
                return "bad"
        else:
            # Si l'employé n'existe pas
            return False

    def hacher_mot_de_passe(self, mot_de_passe):
            return hashlib.sha256(mot_de_passe.encode()).hexdigest()
        
    def créer_premier_employé(self,username, password):
        password = self.hacher_mot_de_passe(password)
        try:
            self.db_manager.execute_update("""
                INSERT INTO Employes (prenom, nom, username, mot_de_passe, poste)
                VALUES (?, ?, ?, ?, ?)
            """, ("temp", "temp", username, password, "Gérant Global"))
            
            self.db_manager.execute_update("""
                INSERT INTO Succursales (nom)
                VALUES (?)
            """, ("temp",))
            

            db_manager = DatabaseManager('erp_database.db')
            
            values = (
                1, 1, 
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00"
            )

            query = """
                        INSERT INTO Horaires (id_employe, id_succursale, date,
                                            heure_entree_lundi, heure_sortie_lundi,
                                            heure_entree_mardi, heure_sortie_mardi,
                                            heure_entree_mercredi, heure_sortie_mercredi,
                                            heure_entree_jeudi, heure_sortie_jeudi,
                                            heure_entree_vendredi, heure_sortie_vendredi, statut)
                        VALUES (?, ?, date('now'),
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'actif')
                    """
            
            db_manager.execute_update(query, values)
            
        except Exception as e:
            print(e)
            
    def update_mdp(self,username, password):
        password = self.hacher_mot_de_passe(password)
        try:
            self.db_manager.execute_update("""
                UPDATE Employes
                SET mot_de_passe = ?
                WHERE username = ?
            """, (password, username))
        except Exception as e:
            print(e)
        
        
    def get_poste(self, username):
        resultat = self.db_manager.execute_query("SELECT poste FROM Employes WHERE username = ?", (username,))
        if resultat:
            return resultat[0][0]
        
    
    def get_succursales(self, username):
        # Étape 1: Récupérer l'ID de l'employé à partir du username
        query = """
        SELECT id_employe FROM Employes WHERE username = ?
        """
        result = self.db_manager.execute_query(query, (username,))
        
        if not result:
            return None  # L'employé avec ce username n'existe pas
        
        # Récupérer l'ID de l'employé
        id_employe = result[0][0]
        
        # Étape 2: Récupérer les succursales associées à cet employé via la table Employes_Succursales
        query = """
        SELECT Succursales.id_succursale
        FROM Employes_Succursales
        JOIN Succursales ON Employes_Succursales.id_succursale = Succursales.id_succursale
        WHERE Employes_Succursales.id_employe = ?
        """
        
        # Exécuter la requête pour récupérer les succursales de l'employé
        succursales = self.db_manager.execute_query(query, (id_employe,))
        
        if not succursales:
            return None  # Aucun résultat trouvé, l'employé n'est pas affecté à une succursale
        
        succursale = succursales[0][0]
        print(succursale)

        return succursale
        
    
    def creer_vente(self, item, quantite, prix_unitaire, date):
        # Simule une requête pour créer une vente
        vente_data = {
            'item': item,
            'quantite': quantite,
            'prix_unitaire': prix_unitaire,
            'date': date
        }
        try:
            response = requests.post('http://localhost:5000/vente', json=vente_data)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return False
    
#     def creer_vente(self, item, quantite, prix_unitaire, date):
#     # Insère une nouvelle vente dans la base de données
#     query = """
#     INSERT INTO Commandes_Produits (id_commande, id_produit, quantite, prix_unitaire, total_ligne)
#     VALUES (?, ?, ?, ?, ?)
#     """
#     # Vous devez gérer l'insertion dans la table Commandes et récupérer id_commande
#     # Pour cet exemple, supposons que id_commande est 1
#     id_commande = 1
#     id_produit = self.get_produit_id(item)
#     total_ligne = quantite * prix_unitaire
#     parameters = (id_commande, id_produit, quantite, prix_unitaire, total_ligne)
#     try:
#         rows_affected = self.db_manager.execute_update(query, parameters)
#         return rows_affected > 0
#     except sqlite3.Error as e:
#         print("Erreur lors de la création de la vente :", e)
#         return False

# def get_produit_id(self, nom_produit):
#     # Récupère l'id du produit à partir de son nom
#     query = "SELECT id_produit FROM Produits WHERE nom_produit = ?"
#     parameters = (nom_produit,)
#     try:
#         result = self.db_manager.execute_query(query, parameters)
#         if result:
#             return result[0]['id_produit']
#         else:
#             print("Produit non trouvé :", nom_produit)
#             return None
#     except sqlite3.Error as e:
#         print("Erreur lors de la récupération de l'id du produit :", e)
#         return None
