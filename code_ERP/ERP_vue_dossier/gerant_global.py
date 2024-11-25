from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class QGerantGlobal(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.setStyleSheet("QPushButton{padding: 10px; background-color:white; border:2px solid black;}  QPushButton:pressed{background-color:#cacccf;}")

        # Titre de la fenêtre
        self.setWindowTitle("Gérant global")
        
        # Création des boutons
        button1 = QPushButton("Succursale")
        button1.clicked.connect(parent.basculer_vers_succursale)
        
        button2 = QPushButton("Ajout de champ")
        button2.clicked.connect(parent.basculer_vers_ajout_champ)
        
        button3 = QPushButton("Règle d'affaire")
        
        button4 = QPushButton("HR")
        button4.clicked.connect(parent.basculer_vers_hr)
        
        button5 = QPushButton("Gérer employé")
        button5.clicked.connect(parent.basculer_vers_gerer_employe)
        
        # Mise en page horizontale pour les boutons centrés
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.addWidget(button4)
        button_layout.addWidget(button5)

        # Ajouter du padding entre les boutons
        button_layout.setSpacing(30)  # Espacement entre les boutons
        button_layout.setContentsMargins(50, 50, 50, 50)  # Marges de la mise en page

        # Centrer le layout dans la fenêtre
        button_layout.setAlignment(Qt.AlignCenter)

        # Layout principal
        main_layout = QVBoxLayout()

        # Bouton en haut à droite
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        back_button.setFixedSize(70, 50)  # Ajustez la taille du bouton si nécessaire

        # Layout pour le bouton de retour
        back_button_layout = QHBoxLayout()
        back_button_layout.addWidget(back_button)
        back_button_layout.addStretch()  # Pour pousser le bouton à droite

        # Ajouter les layouts au layout principal
        main_layout.addLayout(back_button_layout)  # Bouton en haut à droite
        main_layout.addLayout(button_layout)  # Autres boutons centrés

        # Appliquer le layout principal à la fenêtre
        self.setLayout(main_layout)
