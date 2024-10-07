from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
import sys
import requests
from ERP_modele import Modele
from ERP_vue import Vue
from ERP_data_base import DatabaseManager

class Controleur:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.modele = Modele(self.db_manager)
        self.vue = Vue(self)
        
    def se_connecter(self):
        username, password = self.vue.obtenir_identifiants()
        if self.modele.verifier_identifiants(username, password):
            #VERIFIER LE ROLE DE L'UTILISATEUR ET LE BASCULER SUR LA PAGE DE SON ROLE
            self.vue.afficher_message("Succès", "Connexion réussie !")
            self.vue.basculer_vers_splash()
        else:
            self.vue.afficher_message("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def enregistrer_vente(self):
        item, quantite, prix_unitaire, date = self.vue.obtenir_informations_vente()
        if self.modele.creer_vente(item, quantite, prix_unitaire, date):
            self.vue.afficher_message("Succès", "Vente enregistrée avec succès.")
        else:
            self.vue.afficher_message("Erreur", "Erreur lors de l'enregistrement de la vente.")

    def annuler_vente(self):
        self.vue.basculer_vers_splash()

    def action_splash(self, action):
        if action == "gestion":
            self.vue.afficher_message("Gestion interne", "Fonctionnalité non implémentée")
        elif action == "options":
            self.vue.afficher_message("Options d'utilisation", "Fonctionnalité non implémentée")
        elif action == "formulaire":
            self.vue.basculer_vers_vente()
        elif action == "stock":
            self.vue.basculer_vers_stock()
        elif action == "Produit":
            self.vue.basculer_vers_produit()

    def demarrer(self):
        self.vue.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        db_manager = DatabaseManager('erp_database.db')
        print("Les tables ont été créées avec succès.")
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Erreur", f"Une erreur est survenue lors de l'initialisation de la base de données : {e}")
        sys.exit(1)

    controleur = Controleur(db_manager)
    controleur.demarrer()
    sys.exit(app.exec())
