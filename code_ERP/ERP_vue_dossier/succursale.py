from PySide6.QtWidgets import  QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

from utils.QListe import QListe

class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle("Page Succursale")

        # Création des boutons
        back_button = QPushButton("Back")
        back_button.clicked.connect(parent.basculer_vers_gerant_global)
        ajouter_button = QPushButton("Ajouter")
        modifier_button = QPushButton("Modifier")
        retirer_button = QPushButton("Retirer")

        # Mise en page principale
        main_layout = QHBoxLayout()  # Utiliser un layout horizontal

        # Mise en page pour tous les boutons
        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button, alignment=Qt.AlignTop)  # Bouton Back en haut

        # Espacement pour centrer les autres boutons
        button_layout.addStretch()  # Ajout d'un étirement pour espacer le bouton Back des autres
        button_layout.addWidget(ajouter_button)
        button_layout.addWidget(modifier_button)
        button_layout.addWidget(retirer_button)
        button_layout.addStretch()  # Ajout d'un étirement pour espacer le bouton Back des autres

        # Ajouter du padding entre les boutons
        button_layout.setSpacing(10)  # Espacement entre les boutons
        button_layout.setAlignment(Qt.AlignLeft)  # Aligner à gauche

        # Ajouter le layout des boutons au layout principal
        main_layout.addLayout(button_layout)

        # Ajout d'un espace flexible pour pousser la QListe à droite
        main_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Créer la QListe à droite
        section_names = ["Nom", "Type", "Quantité"]  # Exemple de noms de sections
        objects = []  # Remplissez cette liste avec les objets que vous souhaitez afficher
        liste = QListe("Liste d'Objets", objects, section_names)

        # Ajouter la QListe au layout principal
        main_layout.addWidget(liste, alignment=Qt.AlignCenter)  # Centrer la QListe à droite

        # Appliquer le layout principal à la fenêtre
        self.setLayout(main_layout)