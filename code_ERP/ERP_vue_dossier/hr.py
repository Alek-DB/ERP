from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class qHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("QPushButton{padding: 10px; background-color:white; border:2px solid black;} QPushButton:pressed{background-color:#cacccf;}")

        # Title and Layout
        self.setWindowTitle("Gestion des Ressources Humaines")
        
        # Création des boutons
        button1 = QPushButton("Employés")
        button1.clicked.connect(parent.basculer_vers_employes_hr)
        #employe_button.clicked.connect(parent.basculer_vers_succursale)
        
        button2 = QPushButton("Commandes")
        #commandes_button.clicked.connect(parent.basculer_vers_ajout_champ)
        button2.clicked.connect(parent.basculer_vers_commandes_hr)
        
        # Back Button
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)


         # Mise en page horizontale
        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(back_button)

      
        # Ajouter du padding entre les boutons
        layout.setSpacing(30)  # Espacement entre les boutons
        layout.setContentsMargins(50, 50, 50, 50)  # Marges de la mise en page

        # Centrer le layout dans la fenêtre
        layout.setAlignment(Qt.AlignCenter)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)