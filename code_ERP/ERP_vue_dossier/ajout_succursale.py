from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit
)
from PySide6.QtCore import Qt

from PySide6.QtCore import Qt

class QAjouterSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.vue = parent

        # Titre de la fenêtre
        self.setWindowTitle("Ajouter Succursale")

        # Mise en page principale
        main_layout = QVBoxLayout()
        
        # Mise en page pour le bouton Back
        back_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.vue.basculer_vers_succursale)
        back_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        main_layout.addLayout(back_layout)

        # Mise en page pour les champs de saisie
        form_layout = QVBoxLayout()

        # Champ pour le nom
        nom_layout = QHBoxLayout()
        nom_label = QLabel("Nom:")
        nom_input = QTextEdit()
        nom_input.setFixedSize(200, 30)  # Largeur fixe et hauteur réduite
        nom_layout.addWidget(nom_label, alignment=Qt.AlignCenter)
        nom_layout.addWidget(nom_input, alignment=Qt.AlignCenter)
        nom_layout.setSpacing(0)  # Supprimer l'espace entre le label et la zone de texte
        form_layout.addLayout(nom_layout)

        # Champ pour l'adresse
        adresse_layout = QHBoxLayout()
        adresse_label = QLabel("Adresse:")
        adresse_input = QTextEdit()
        adresse_input.setFixedSize(200, 30)  # Largeur fixe et hauteur réduite
        adresse_layout.addWidget(adresse_label, alignment=Qt.AlignCenter)
        adresse_layout.addWidget(adresse_input, alignment=Qt.AlignCenter)
        adresse_layout.setSpacing(0)  # Supprimer l'espace entre le label et la zone de texte
        form_layout.addLayout(adresse_layout)

        # Champ pour le code
        code_layout = QHBoxLayout()
        code_label = QLabel("Code:")
        code_input = QTextEdit()
        code_input.setFixedSize(200, 30)  # Largeur fixe et hauteur réduite
        code_layout.addWidget(code_label, alignment=Qt.AlignCenter)
        code_layout.addWidget(code_input, alignment=Qt.AlignCenter)
        code_layout.setSpacing(0)  # Supprimer l'espace entre le label et la zone de texte
        form_layout.addLayout(code_layout)

        # Centrer le formulaire
        form_layout.setAlignment(Qt.AlignCenter)

        # Ajouter le formulaire au layout principal
        main_layout.addLayout(form_layout)

        # Bouton Confirmer
        self.confirm_button = QPushButton("Confirmer")
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignRight)  # Aligné à droite en bas
        self.confirm_button.clicked.connect(self.enregistrer_information)

        # Appliquer le layout principal à la fenêtre
        self.setLayout(main_layout)
        
        
    def enregistrer_information(self):
        ## for tout les champs, rajouter dans la table
        
        if self.confirm_button.text() == "Modifier":
            print("modif")
        else:
            print("ajout")
            
        self.vue.basculer_vers_succursale()
        
    
    def set_to_modif(self):
        self.confirm_button.setText("Modifier")
    
    def set_to_ajout(self):
        self.confirm_button.setText("Ajouter")