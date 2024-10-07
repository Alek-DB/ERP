from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QStackedWidget, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt

from ERP_vue_dossier.gerant_global import QGerantGlobal
from ERP_vue_dossier.succursale import QSuccursale
<<<<<<< HEAD
from ERP_vue_dossier.stock import QStock

=======
from ERP_vue_dossier.ajout_succursale import QAjouterSuccursale
>>>>>>> 306cd06c02481665caded28c0d2bbd2f979a4916

# La classe Modele reste inchangée

class Vue(QMainWindow):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Application ERP")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.frame_connexion = self.creer_frame_connexion()
        self.frame_vente = self.creer_frame_vente()
        self.frame_stock = QStock(self)
        self.frame_splash = self.creer_frame_splash()
        self.frame_greant_global = QGerantGlobal(self)
        self.frame_succursale = QSuccursale(self)
        self.frame_ajout_succursale = QAjouterSuccursale(self)

        self.stacked_widget.addWidget(self.frame_connexion)
        self.stacked_widget.addWidget(self.frame_splash)
        self.stacked_widget.addWidget(self.frame_vente)
<<<<<<< HEAD
        self.stacked_widget.addWidget(self.frame_stock)

        #self.stacked_widget.addWidget(self.frame_greant_global)
        #self.stacked_widget.addWidget(self.frame_succursale )
=======
        self.stacked_widget.addWidget(self.frame_greant_global)
        self.stacked_widget.addWidget(self.frame_succursale)
        self.stacked_widget.addWidget(self.frame_ajout_succursale)
>>>>>>> 306cd06c02481665caded28c0d2bbd2f979a4916

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
        self.button_formulaire = QPushButton("Stock")
        self.button_formulaire.clicked.connect(lambda: self.controleur.action_splash("stock"))

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
        
    def basculer_vers_stock(self):
        self.stacked_widget.setCurrentWidget(self.frame_stock)
        
    def basculer_vers_succursale(self):
        self.stacked_widget.setCurrentWidget(self.frame_succursale)
<<<<<<< HEAD
        
    def basculer_vers_gerant_global(self):
        self.stacked_widget.setCurrentWidget(self.frame_greant_global)
=======
    
    def basculer_vers_ajout_succursale(self, ajout):
        if ajout:
            self.frame_ajout_succursale.set_to_ajout()
        else:
            self.frame_ajout_succursale.set_to_modif()
        self.stacked_widget.setCurrentWidget(self.frame_ajout_succursale)
>>>>>>> 306cd06c02481665caded28c0d2bbd2f979a4916

    def obtenir_identifiants(self):
        return self.entry_username.text(), self.entry_password.text()

    def obtenir_informations_vente(self):
        return (self.entry_item.text(),
                self.entry_quantite.text(),
                self.entry_prix.text(),
                self.entry_date.text())