from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
import sys
import sqlite3
import requests
from ERP_modele import Modele
from ERP_vue import Vue
from ERP_data_base import DatabaseManager



"""
+----------------------------------------------------+
|                                                    |
|                   USERNAME: emp                    |
|                  MOT DE PASSE: AAAaaa111           |
|                                                    |
+----------------------------------------------------+
"""


class Controleur:
    def __init__(self, db_manager): 
        self.db_manager = db_manager
        self.modele = Modele(self.db_manager)
        self.vue = Vue(self)
        
    def se_connecter(self):
        username, password = self.vue.frame_connexion.obtenir_identifiants()
         
        state = self.modele.verifier_identifiants(username, password)
        
        if state == "good":
            #VERIFIER LE ROLE DE L'UTILISATEUR ET LE BASCULER SUR LA PAGE DE SON ROLE
            self.vue.afficher_message("Succès", "Connexion réussie !")
            poste = self.modele.get_poste(username) #basculer selon poste
            if poste == "Gérant global":pass
            elif poste == "Employé":pass
            elif poste == "Gérant":pass
            self.vue.basculer_vers_splash()  
            
        elif state == "bad":    # employé existe mais mauvais mot de passe
            self.vue.afficher_message("Erreur", "Mot de passe incorrect.")
        else:
            if self.vue.frame_connexion.first_login: # Employé n'existe pas et premier
                confirmation_dialog = QMessageBox()
                confirmation_dialog.setWindowTitle("Première connexion")
                confirmation_dialog.setText(f"Voullez vous continuer avec ce mot de passe ?")
                confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirmation_dialog.setIcon(QMessageBox.Warning)
                # Si l'utilisateur confirme le mdp
                if confirmation_dialog.exec_() == QMessageBox.Yes:
                    try:
                        self.modele.créer_premier_employé(username, password)
                        self.vue.basculer_vers_splash()
                    except Exception as e:
                        print(e)
            else:   # Employé n'existe pas et pas premier
                self.vue.afficher_message("Erreur", "Aucun employé de ce nom")

    def enregistrer_vente(self):
        item, quantite, prix_unitaire, date = self.vue.obtenir_informations_vente()
        if self.modele.creer_vente(item, quantite, prix_unitaire, date):
            self.vue.afficher_message("Succès", "Vente enregistrée avec succès.")
        else:
            self.vue.afficher_message("Erreur", "Erreur lors de l'enregistrement de la vente.")

    def annuler_vente(self):
        self.vue.basculer_vers_splash()

    def action_splash(self, action):
        if action == "formulaire":
            self.vue.basculer_vers_vente()
        elif action == "stock":
            self.vue.basculer_vers_stock()
        elif action == "produit":
            self.vue.basculer_vers_produit()
        elif action == "fournisseur":
            self.vue.basculer_vers_fournisseur()
        elif action == "succursale":
            self.vue.basculer_vers_succursale()
        elif action == "gérant global":
            self.vue.basculer_vers_gerant_global()
            
        # Gerant   
        elif action == "gérant":
            self.vue.basculer_vers_gerant()
        # HR
        elif action == "hr":
            self.vue.basculer_vers_hr()
        # HR Commandes
        elif action == "hr commandes":
            self.vue.basculer_vers_hr_commandes()    
        # HR Commandes
        elif action == "hr employes":
            self.vue.basculer_vers_hr_employes()  
            
    def demarrer(self):
        self.vue.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        db_manager = DatabaseManager('erp_database.db')

        # Requête SQL pour récupérer tous les employés
        
        #SUPPRIMER LES EMPLOYÉS ET RESET LE ID
        
        db_manager.execute_update("DELETE FROM Succursales")
        query = "SELECT id_employe, nom, prenom, username, poste FROM Employes"
        results = db_manager.execute_query(query)

        if results:
            # Affichage des résultats dans la console avec print
            print(f"{'id':<20} {'Nom':<20} {'Prénom':<20} {'Username':<20} {'Poste':<20}")
            print("-" * 80)  # Séparateur pour améliorer la lisibilité
            for row in results:
                id, nom, prenom, username, poste = row
                print(f"{id:<20} {nom:<20} {prenom:<20} {username:<20} {poste:<20}")

        else:
            print("Aucun employé trouvé dans la base de données.")
            
        # Supprimer toutes les lignes de la table
        db_manager.execute_query(f"DELETE FROM Employes")
        # Réinitialiser le compteur AUTOINCREMENT à 0
        db_manager.execute_query(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = ?", ("Employes",))
        
        print(f"Le compteur AUTOINCREMENT de la table Employes a été réinitialisé à 0.")
        


        # # Étape 1: Désactiver la vérification des clés étrangères
        # db_manager.execute_update("PRAGMA foreign_keys=OFF")

        # # Étape 2: Supprimer la table existante si elle existe
        # db_manager.execute_update("DROP TABLE IF EXISTS Employes")

        # # Étape 3: Créer la nouvelle table Employes
        # db_manager.execute_update('''
        #     CREATE TABLE IF NOT EXISTS Employes (
        #         id_employe INTEGER PRIMARY KEY AUTOINCREMENT,
        #         prenom TEXT NOT NULL,
        #         nom TEXT NOT NULL,
        #         poste TEXT,
        #         salaire REAL,
        #         date_naissance TEXT,
        #         date_embauche TEXT,
        #         sexe TEXT CHECK(sexe IN ('M', 'F')),
        #         statut TEXT,
        #         allergies_preferences_alimentaires TEXT,
        #         mot_de_passe TEXT,
        #         username TEXT NOT NULL UNIQUE
        #     )
        # ''')

        # # Étape 4: Réactiver la vérification des clés étrangères
        # db_manager.execute_update("PRAGMA foreign_keys=ON")

    except sqlite3.Error as e:
        QMessageBox.critical(None, "Erreur", f"Une erreur est survenue lors de l'initialisation de la base de données : {e}")

    controleur = Controleur(db_manager)
    controleur.demarrer()
    sys.exit(app.exec())
