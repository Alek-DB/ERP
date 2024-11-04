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
        if self.vue.frame_connexion.first_login:
            self.modele.créer_premier_employé(username,password)
        
        state = self.modele.verifier_identifiants(username, password)
        if state == "good":
            #VERIFIER LE ROLE DE L'UTILISATEUR ET LE BASCULER SUR LA PAGE DE SON ROLE
            self.vue.afficher_message("Succès", "Connexion réussie !")
            poste = self.modele.get_poste(username) #basculer selon poste
            if poste == "Gérant global":pass
            elif poste == "Employé":pass
            elif poste == "Gérant":pass
            
            self.vue.basculer_vers_splash()
        elif state == "bad":
            self.vue.afficher_message("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            confirmation_dialog = QMessageBox()
            confirmation_dialog.setWindowTitle("Première connexion")
            confirmation_dialog.setText(f"Voullez vous continuer avec ce mot de passe ?")
            confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation_dialog.setIcon(QMessageBox.Warning)

            # Si l'utilisateur confirme le mdp
            if confirmation_dialog.exec_() == QMessageBox.Yes:
                try:
                    self.db_manager.execute_update("""
                    UPDATE Employes
                    SET mot_de_passe = ?
                    WHERE username = ?
                        """, (self.modele.hacher_mot_de_passe(password) ,username))
                except Exception as e:
                    print(e)

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
            
    def demarrer(self):
        self.vue.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        db_manager = DatabaseManager('erp_database.db')
        #db_manager.execute_update("DELETE FROM Employes")
        


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
        sys.exit(1)

    controleur = Controleur(db_manager)
    controleur.demarrer()
    sys.exit(app.exec())
