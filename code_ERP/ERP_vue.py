from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QStackedWidget
)
from PySide6.QtCore import Qt

# Importation des classes nécessaires
from ERP_vue_dossier.gerant_global import QGerantGlobal
from ERP_vue_dossier.succursale import QSuccursale
from ERP_vue_dossier.stock import QStock
from ERP_vue_dossier.gerant import QGerant
from ERP_vue_dossier.connexion import QConnexion
from ERP_vue_dossier.add_employe import QAddEmploye
from ERP_vue_dossier.ajout_champ import QAjoutChamp
from ERP_emplacement import Emplacement

# La classe Modele reste inchangée

from ERP_vue_dossier.produit import QProduit
from ERP_vue_dossier.fournisseur import QFournisseur


class Vue(QMainWindow):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Application ERP")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Création des différents frames
        self.frame_connexion = QConnexion(self)
        self.frame_vente = self.creer_frame_vente()
        self.frame_stock = QStock(self)
        self.frame_produit = QProduit(self, self.controleur.db_manager)
        self.frame_splash = self.creer_frame_splash()
        self.frame_greant_global = QGerantGlobal(self)
        self.frame_succursale = QSuccursale(self)
        self.frame_fournisseur = QFournisseur(self, self.controleur.db_manager)
        self.frame_gerant = QGerant(self)
        self.frame_ajouter_employe = QAddEmploye(self)
        self.frame_ajout_champ = QAjoutChamp(self)

        # Ajout des frames au QStackedWidget
        self.stacked_widget.addWidget(self.frame_connexion)
        self.stacked_widget.addWidget(self.frame_splash)
        self.stacked_widget.addWidget(self.frame_vente)
        self.stacked_widget.addWidget(self.frame_stock)
        self.stacked_widget.addWidget(self.frame_greant_global)
        self.stacked_widget.addWidget(self.frame_succursale)
        self.stacked_widget.addWidget(self.frame_gerant)


        self.stacked_widget.addWidget(self.frame_produit)
        self.stacked_widget.addWidget(self.frame_fournisseur)
        self.stacked_widget.addWidget(self.frame_ajouter_employe)
        self.stacked_widget.addWidget(self.frame_ajout_champ)
        
        
        self.history = []
        # Affichage initial
        self.basculer_vers_connexion()

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
        self.button_formulaire = QPushButton("Formulaire")
        self.button_formulaire.clicked.connect(lambda: self.controleur.action_splash("formulaire"))
        self.button_stock = QPushButton("Stock")
        self.button_stock.clicked.connect(lambda: self.controleur.action_splash("stock"))
        self.button_produit = QPushButton("Produit")
        self.button_produit.clicked.connect(lambda: self.controleur.action_splash("produit"))
        self.button_fournisseur = QPushButton("Fournisseur")
        self.button_fournisseur.clicked.connect(lambda: self.controleur.action_splash("fournisseur"))
        self.button_fournisseur = QPushButton("Succursale")
        self.button_fournisseur.clicked.connect(lambda: self.controleur.action_splash("succursale"))
        self.button_fournisseur = QPushButton("Gérant global")
        self.button_fournisseur.clicked.connect(lambda: self.controleur.action_splash("gérant global"))
        
        buttons_layout.addWidget(self.button_formulaire)
        buttons_layout.addWidget(self.button_stock)
        buttons_layout.addWidget(self.button_produit)
        buttons_layout.addWidget(self.button_fournisseur)

        layout.addLayout(buttons_layout)

        widget.setLayout(layout)
        return widget


    def afficher_message(self, titre, message):
        QMessageBox.information(self, titre, message)

    # Méthodes pour basculer entre les frames
    def basculer_vers_connexion(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_connexion)

    def basculer_vers_splash(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_splash)

    def basculer_vers_vente(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_vente)

    def basculer_vers_stock(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_stock)

    def basculer_vers_succursale(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_succursale)

    def basculer_vers_produit(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_produit)
        
    def basculer_vers_gerant_global(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_greant_global)

    def basculer_vers_fournisseur(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_fournisseur)
    
    def basculer_vers_ajouter_employer(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_ajouter_employe)
    
    def basculer_vers_gerant(self, code): # baculer vers la succursale
        self.history.append(self.stacked_widget.currentWidget())
        Emplacement.succursalesCode = code
        self.stacked_widget.setCurrentWidget(self.frame_gerant)
        
    def basculer_before(self):
        if self.history:
            previous_widget = self.history.pop()  # Retirer le dernier widget visité
            self.stacked_widget.setCurrentWidget(previous_widget)
    
    def basculer_vers_ajout_champ(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_ajout_champ)





    # Méthodes pour obtenir les informations saisies par l'utilisateur

    def obtenir_informations_vente(self):
        return (
            self.entry_item.text(),
            self.entry_quantite.text(),
            self.entry_prix.text(),
            self.entry_date.text()
        )
