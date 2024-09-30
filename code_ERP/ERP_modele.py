import requests

class Modele:
    def __init__(self):
        self.authenticated = False

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