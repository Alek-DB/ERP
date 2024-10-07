import requests
from ERP_data_base import DatabaseManager

class Modele:
    def __init__(self,db_manager):
        self.authenticated = False
        self.db_manager = db_manager

    def verifier_identifiants(self, username, password):
        # Simule une requête au serveur pour vérifier les identifiants
        try:
            response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200 and response.json().get('success'):
                self.authenticated = True
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return False

    # def verifier_identifiants(self, username, password):
    # # Vérifie les identifiants dans la base de données
    # query = "SELECT * FROM Employes WHERE code_unique = ? AND password = ?"
    # parameters = (username, password)
    # try:
    #     result = self.db_manager.execute_query(query, parameters)
    #     if result:
    #         self.authenticated = True
    #         # Vous pouvez stocker des informations supplémentaires sur l'utilisateur
    #         self.utilisateur = result[0]
    #         return True
    #     else:
    #         return False
    # except sqlite3.Error as e:
    #     print("Erreur lors de la vérification des identifiants :", e)
    #     return False

    
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
