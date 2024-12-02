from PySide6.QtWidgets import  QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QLineEdit
from PySide6.QtCore import Qt

from ERP_emplacement import Emplacement
from ERP_data_base import DatabaseManager


class QConnexion(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.db_manager = DatabaseManager('erp_database.db')
        
        layout = QVBoxLayout()
        
        self.first_login = self.is_table_empty()
        
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
        
        if(self.first_login): form_layout.addWidget(QLabel("Créer votre mot de passe"), 1, 0)
        else: form_layout.addWidget(QLabel("Mot de passe"), 1, 0)
        form_layout.addWidget(self.entry_password, 1, 1)

        layout.addLayout(form_layout)

        if(self.first_login): self.button_login = QPushButton("Créer son compte")
        else: self.button_login = QPushButton("Se connecter")
        self.button_login.clicked.connect(parent.controleur.se_connecter)
        layout.addWidget(self.button_login)

        self.setLayout(layout)
        
        
    def is_table_empty(self):
        count = self.db_manager.execute_query("SELECT COUNT(*) FROM Employes")
        return count[0][0] == 0  # Retourne True si la table est vide
    
    def obtenir_identifiants(self):
        return self.entry_username.text(), self.entry_password.text()