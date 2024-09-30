from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
import sys
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


from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QStackedWidget)
from PySide6.QtCore import Qt
import sys
import requests

# La classe Modele reste inchangée

class Vue(QMainWindow):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Application ERP")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.frame_connexion = self.creer_frame_connexion()
        self.frame_vente = self.creer_frame_vente()
        self.frame_splash = self.creer_frame_splash()

        self.stacked_widget.addWidget(self.frame_connexion)
        self.stacked_widget.addWidget(self.frame_splash)
        self.stacked_widget.addWidget(self.frame_vente)

        # Affichage initial
        self.basculer_vers_connexion()

    def creer_frame_connexion(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titre = QLabel("Connexion ERP")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titre)

        form_layout = QGridLayout()
        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel("Nom d'utilisateur"), 0, 0)
        form_layout.addWidget(self.entry_username, 0, 1)
        form_layout.addWidget(QLabel("Mot de passe"), 1, 0)
        form_layout.addWidget(self.entry_password, 1, 1)

        layout.addLayout(form_layout)

        self.button_login = QPushButton("Se connecter")
        self.button_login.clicked.connect(self.controleur.se_connecter)
        layout.addWidget(self.button_login)

        widget.setLayout(layout)
        return widget

    def creer_frame_vente(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titre = QLabel("Enregistrement des ventes")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titre)

        explication = QLabel("Veuillez remplir les champs ci-dessous pour enregistrer une nouvelle vente.")
        explication.setWordWrap(True)
        layout.addWidget(explication)

        form_layout = QGridLayout()
        self.entry_item = QLineEdit()
        self.entry_quantite = QLineEdit()
        self.entry_prix = QLineEdit()
        self.entry_date = QLineEdit()

        form_layout.addWidget(QLabel("Article"), 0, 0)
        form_layout.addWidget(self.entry_item, 0, 1)
        form_layout.addWidget(QLabel("Quantité"), 1, 0)
        form_layout.addWidget(self.entry_quantite, 1, 1)
        form_layout.addWidget(QLabel("Prix Unitaire"), 2, 0)
        form_layout.addWidget(self.entry_prix, 2, 1)
        form_layout.addWidget(QLabel("Date"), 3, 0)
        form_layout.addWidget(self.entry_date, 3, 1)

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        self.button_enregistrer_vente = QPushButton("Accepter vente")
        self.button_enregistrer_vente.clicked.connect(self.controleur.enregistrer_vente)
        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.clicked.connect(self.controleur.annuler_vente)
        buttons_layout.addWidget(self.button_enregistrer_vente)
        buttons_layout.addWidget(self.button_annuler)

        layout.addLayout(buttons_layout)

        widget.setLayout(layout)
        return widget

    def creer_frame_splash(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titre = QLabel("ERP Manager")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titre)

        sous_titre = QLabel("Système de gestion intégré pour votre entreprise")
        sous_titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(sous_titre)

        buttons_layout = QHBoxLayout()
        self.button_gestion = QPushButton("Gestion interne")
        self.button_gestion.clicked.connect(lambda: self.controleur.action_splash("gestion"))
        self.button_options = QPushButton("Options d'utilisation")
        self.button_options.clicked.connect(lambda: self.controleur.action_splash("options"))
        self.button_formulaire = QPushButton("Formulaire")
        self.button_formulaire.clicked.connect(lambda: self.controleur.action_splash("formulaire"))

        buttons_layout.addWidget(self.button_gestion)
        buttons_layout.addWidget(self.button_options)
        buttons_layout.addWidget(self.button_formulaire)

        layout.addLayout(buttons_layout)

        widget.setLayout(layout)
        return widget

    def afficher_message(self, titre, message):
        QMessageBox.information(self, titre, message)

    def basculer_vers_connexion(self):
        self.stacked_widget.setCurrentWidget(self.frame_connexion)

    def basculer_vers_splash(self):
        self.stacked_widget.setCurrentWidget(self.frame_splash)

    def basculer_vers_vente(self):
        self.stacked_widget.setCurrentWidget(self.frame_vente)

    def obtenir_identifiants(self):
        return self.entry_username.text(), self.entry_password.text()

    def obtenir_informations_vente(self):
        return (self.entry_item.text(),
                self.entry_quantite.text(),
                self.entry_prix.text(),
                self.entry_date.text())

# Les classes Controleur et le code de démarrage restent inchangés

class Controleur:
    def __init__(self):
        self.modele = Modele()
        self.app = QApplication(sys.argv)
        self.vue = Vue(self)

    def se_connecter(self):
        username, password = self.vue.obtenir_identifiants()
        if self.modele.verifier_identifiants(username, password):
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

    def demarrer(self):
        self.vue.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = Controleur()
    app.demarrer()