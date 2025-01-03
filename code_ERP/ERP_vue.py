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
from ERP_vue_dossier.employe import QEmploye
from ERP_vue_dossier.connexion import QConnexion
from ERP_vue_dossier.add_employe import QAddEmploye
from ERP_vue_dossier.ajout_champ import QAjoutChamp
from ERP_vue_dossier.gerer_employe import QGereEmploye
from ERP_vue_dossier.horaire import QHoraire
from ERP_vue_dossier.regle_affaire import QRegleAffaire
from ERP_emplacement import Emplacement
from ERP_vue_dossier.hr import qHRWindow
from ERP_vue_dossier.commandes_hr import CommandesHRWindow
from ERP_vue_dossier.employe_hr import EmployeHRWindow
from ERP_vue_dossier.client import QClient

# La classe Modele reste inchangée

from ERP_vue_dossier.produit import QProduit
from ERP_vue_dossier.fournisseur import QFournisseur
from ERP_vue_dossier.finance import QFinance
from ERP_vue_dossier.rapport_finance import QFinanceReport
from ERP_vue_dossier.rapport_finance_fournisseur import QFinanceFournisseurReport
from ERP_vue_dossier.commande_fournisseur import QCommandeFournisseur
from ERP_vue_dossier.afficher_regle import QAfficheRegle



class Vue(QMainWindow):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Application ERP")
        self.setGeometry(100, 100, 800, 600)


        main_widget = QWidget()
        main_widget.setObjectName("main")
        self.setCentralWidget(main_widget)
        main_widget.setStyleSheet("""#main{background-color:'white'} 
                                  QPushButton{padding: 10px; background-color:white; border:2px solid black; width:110px; border-radius:5px}  
                                  QPushButton:pressed{background-color:#cacccf;}""")

        layout = QVBoxLayout(main_widget)

        info_widget = QWidget()
        info_layout = QVBoxLayout()
        info_widget.setObjectName("info")
        info_widget.setStyleSheet("#info{border-radius:10px; border:2px solid black; background-color:'#e6e6e6'} QLabel{font-size: 14px; font-weight: bold;}")
        info_widget.setLayout(info_layout)

        self.username_text = QLabel()
        self.role_text = QLabel()
        self.succursale_text = QLabel()
        info_layout.addWidget(self.username_text)
        info_layout.addWidget(self.role_text)
        info_layout.addWidget(self.succursale_text)

        layout.addWidget(info_widget)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget{background-color:'#e6e6e6'; border-radius:10px; border:2px solid black}")
        layout.addWidget(self.stacked_widget)

        # Création des différents frames
        self.frame_connexion = QConnexion(self)
        self.frame_stock = QStock(self)
        self.frame_produit = QProduit(self, self.controleur.db_manager)
        self.frame_splash = self.creer_frame_splash()
        self.frame_greant_global = QGerantGlobal(self)
        self.frame_succursale = QSuccursale(self)
        self.frame_fournisseur = QFournisseur(self, self.controleur.db_manager)
        self.frame_finance = QFinance(self)
        self.frame_finance_report = QFinanceReport(self, self.controleur.db_manager)
        self.frame_fournisseur_report = QFinanceFournisseurReport(self, self.controleur.db_manager)
        self.frame_fournisseur_commande = QCommandeFournisseur(self, self.controleur.db_manager)

        self.frame_gerant = QGerant(self)
        self.frame_employe = QEmploye(self)
        self.frame_ajouter_employe = QAddEmploye(self)
        self.frame_ajout_champ = QAjoutChamp(self)

        # Frame HR
        self.frame_hr = qHRWindow(self)
        self.frame_hr_commandes = CommandesHRWindow(self)
        self.frame_hr_employe = EmployeHRWindow(self)
        self.frame_gerer_employe = QGereEmploye(self)
        self.frame_horaire = QHoraire(self)
        self.frame_regle_affaire = QRegleAffaire(self)
        self.frame_affiche_regle = QAfficheRegle(self)
        self.frame_gerer_client = QClient(self, self.controleur.db_manager)

        # Ajout des frames au QStackedWidget
        self.stacked_widget.addWidget(self.frame_connexion)
        self.stacked_widget.addWidget(self.frame_splash)
        self.stacked_widget.addWidget(self.frame_stock)
        self.stacked_widget.addWidget(self.frame_greant_global)
        self.stacked_widget.addWidget(self.frame_succursale)
        self.stacked_widget.addWidget(self.frame_finance)
        self.stacked_widget.addWidget(self.frame_finance_report)
        self.stacked_widget.addWidget(self.frame_fournisseur_report)
        self.stacked_widget.addWidget(self.frame_fournisseur_commande)
        self.stacked_widget.addWidget(self.frame_gerant)
        self.stacked_widget.addWidget(self.frame_employe)
        self.stacked_widget.addWidget(self.frame_produit)
        self.stacked_widget.addWidget(self.frame_fournisseur)

        # Frame HR
        self.stacked_widget.addWidget(self.frame_hr)
        self.stacked_widget.addWidget(self.frame_hr_commandes)
        self.stacked_widget.addWidget(self.frame_hr_employe)
        self.stacked_widget.addWidget(self.frame_ajouter_employe)
        self.stacked_widget.addWidget(self.frame_ajout_champ)
        self.stacked_widget.addWidget(self.frame_gerer_employe)
        self.stacked_widget.addWidget(self.frame_horaire)
        self.stacked_widget.addWidget(self.frame_regle_affaire)
        self.stacked_widget.addWidget(self.frame_gerer_client)
        self.stacked_widget.addWidget(self.frame_affiche_regle)
        
        
        self.history = []
        # Affichage initial
        self.basculer_vers_connexion()

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
        self.button_stock = QPushButton("Stock")
        self.button_stock.clicked.connect(lambda: self.controleur.action_splash("stock"))
        self.button_produit = QPushButton("Produit")
        self.button_produit.clicked.connect(lambda: self.controleur.action_splash("produit"))
        self.button_fournisseur = QPushButton("Fournisseur")
        self.button_fournisseur.clicked.connect(lambda: self.controleur.action_splash("fournisseur"))
        self.button_finance = QPushButton("Finance")
        self.button_finance.clicked.connect(lambda: self.controleur.action_splash("finance"))

        buttons_layout.addWidget(self.button_stock)
        buttons_layout.addWidget(self.button_produit)
        buttons_layout.addWidget(self.button_fournisseur)
        buttons_layout.addWidget(self.button_finance)  
        self.button_gerant_global = QPushButton("Gérant global")
        self.button_gerant_global.clicked.connect(lambda: self.controleur.action_splash("gérant global"))
        
       
        # buttons_layout.addWidget(self.button_gerant_global)

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

    def basculer_vers_stock(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_stock)

    def basculer_vers_succursale(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.frame_succursale.load_succursale()
        self.stacked_widget.setCurrentWidget(self.frame_succursale)
        

    def basculer_vers_produit(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_produit)


        
    def basculer_vers_gerant_global(self):
        Emplacement.succursalesId = -1
        self.set_info()
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_greant_global)

    def basculer_vers_ajout_succursale(self, ajout):
        if ajout:
            self.frame_ajout_succursale.set_to_ajout()
        else:
            self.frame_ajout_succursale.set_to_modif()
        self.stacked_widget.setCurrentWidget(self.frame_ajout_succursale)


    def basculer_vers_fournisseur(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_fournisseur)
        
    def basculer_vers_finance(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_finance)
        
    def basculer_vers_finance_report(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.frame_finance_report.set_financial_data()
        self.stacked_widget.setCurrentWidget(self.frame_finance_report)
        
    def basculer_vers_fournisseur_report(self):
        self.history.append(self.stacked_widget.currentWidget())        
        self.stacked_widget.setCurrentWidget(self.frame_fournisseur_report)
        
    def basculer_vers_fournisseur_commandes(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_fournisseur_commande)


    # Méthodes pour obtenir les informations saisies par l'utilisateur
    def obtenir_identifiants(self):
        return self.entry_username.text(), self.entry_password.text()
    
    def basculer_vers_ajouter_employer(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_ajouter_employe)
        
    def basculer_vers_regle_affaire(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_regle_affaire)
    
    def basculer_vers_employe(self, id): # baculer vers la succursale
        self.history.append(self.stacked_widget.currentWidget())
        Emplacement.succursalesId = id
        self.set_info()
        self.stacked_widget.setCurrentWidget(self.frame_employe)
        
    def basculer_vers_gerant(self, id): # baculer vers la succursale
        self.history.append(self.stacked_widget.currentWidget())
        Emplacement.succursalesId = id
        self.set_info()
        self.stacked_widget.setCurrentWidget(self.frame_gerant)
        
    # vers hr    
    def basculer_vers_hr(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_hr) 
    # Vers HR commandes
    def basculer_vers_commandes_hr(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_hr_commandes)
    
    # Vers HR Employées
    def basculer_vers_employes_hr(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_hr_employe)   
    
        
    def basculer_vers_horaire(self, id): # baculer vers la succursale
        self.history.append(self.stacked_widget.currentWidget())
        Emplacement.employeHoraire = id
        #LE SUCCURSALE ID NE VA PAS ETRE BON SI ON EST DANS GERANT GLOBAL
        self.frame_horaire.load_horaires()
        self.stacked_widget.setCurrentWidget(self.frame_horaire)
        
    def basculer_before(self):
        if self.history:
            previous_widget = self.history.pop()  # Retirer le dernier widget visité
            
            if previous_widget == self.frame_greant_global or previous_widget == self.frame_succursale: 
                Emplacement.succursalesId = -1
                self.set_info()
            if previous_widget == self.frame_gerer_employe: 
                self.frame_gerer_employe.load_employe()
            
            self.stacked_widget.setCurrentWidget(previous_widget)
    
    def basculer_vers_ajout_champ(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_ajout_champ)
        
    def basculer_vers_gerer_employe(self):
        self.frame_gerer_employe.load_employe()
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_gerer_employe)
        
    def basculer_vers_gerer_client(self):
        self.history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.frame_gerer_client)


    def basculer_vers_afficher_regles_affaire(self):        
        self.history.append(self.stacked_widget.currentWidget())
        self.frame_affiche_regle.load_data()
        self.stacked_widget.setCurrentWidget(self.frame_affiche_regle)


    def set_info(self):
        self.username_text.setText("Username : " + Emplacement.employeUsername)
        self.role_text.setText("Rôle : " + Emplacement.employeRole)
        self.succursale_text.setText("Succursale : " + str("global" if Emplacement.succursalesId == -1 else Emplacement.succursalesId))