from PySide6.QtWidgets import  QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class QSuccursale(QWidget):
    def __init__(self):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle("Page Succursale")

        # Création des boutons
        back_button = QPushButton("Back")
        ajouter_button = QPushButton("Ajouter")
        modifier_button = QPushButton("Modifier")

        # Mise en page principale
        main_layout = QVBoxLayout()

        # Mise en page pour le bouton Back
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        main_layout.addLayout(back_layout)

        # Mise en page pour les boutons Ajouter et Modifier (alignés verticalement)
        action_layout = QVBoxLayout()  # Utiliser un layout vertical
        action_layout.addWidget(ajouter_button)
        action_layout.addWidget(modifier_button)

        # Ajouter du padding entre les boutons
        action_layout.setSpacing(10)  # Espacement entre les boutons
        action_layout.setAlignment(Qt.AlignLeft)  # Aligner à gauche

        # Ajouter le layout des actions au layout principal
        main_layout.addLayout(action_layout)

        # Appliquer le layout principal à la fenêtre
        self.setLayout(main_layout)