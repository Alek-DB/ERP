from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
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

        button2 = QPushButton("Commandes")
        button2.clicked.connect(parent.basculer_vers_commandes_hr)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        
        button_layout.setSpacing(30)  # Espacement entre les boutons
        button_layout.setContentsMargins(50, 50, 50, 50)  # Marges de la mise en page

        # Centrer le layout dans la fenêtre
        button_layout.setAlignment(Qt.AlignCenter)
        
        
        # Back Button
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        
        back_button_layout = QHBoxLayout()
        back_button_layout.addWidget(back_button)
        back_button_layout.addStretch()  # Pour pousser le bouton à droite


         # Mise en page horizontale
        layout = QVBoxLayout()
        layout.addLayout(back_button_layout)
        layout.addLayout(button_layout)

      
        # Ajouter du padding entre les boutons
        layout.setSpacing(30)  # Espacement entre les boutons
        layout.setContentsMargins(50, 50, 50, 50)  # Marges de la mise en page

        # Centrer le layout dans la fenêtre
        layout.setAlignment(Qt.AlignCenter)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)