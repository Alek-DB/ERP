from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel
)
from PySide6.QtCore import Qt

from utils.QListe import QListe

class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.vue = parent

        # Titre de la fenêtre
        self.setWindowTitle("Page Succursale")

        # Initialiser le mode à aucun
        self.current_mode = None

        # Création des boutons
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.vue.basculer_vers_gerant_global)
        ajouter_button = QPushButton("Ajouter")
        ajouter_button.clicked.connect(lambda: self.vue.basculer_vers_ajout_succursale(True))
        modifier_button = QPushButton("Modifier")
        retirer_button = QPushButton("Retirer")

        # Connecter les boutons à leurs actions respectives
        modifier_button.clicked.connect(lambda: self.set_mode('modifier'))
        retirer_button.clicked.connect(lambda: self.set_mode('retirer'))

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


        section_names = ["Nom", "Adresse", "Nombre d'employé"]  # Exemple de noms de sections
        layout_list = []
        for i in range(10):
            layout_obj = []
            nom = QPushButton("Button")
            nom.clicked.connect(self.handle_button_click)
            layout_obj.append(nom)
            
            addresse = QLabel("addresse")
            layout_obj.append(addresse)
            
            nbEmploye = QLabel("5")
            layout_obj.append(nbEmploye)
            
            layout_list.append(layout_obj) 
        liste = QListe("Liste de succursale", layout_list, section_names)
        main_layout.addWidget(liste, alignment=Qt.AlignCenter)  

        self.setLayout(main_layout)

    def set_mode(self, mode):
        self.current_mode = mode
        for btn in self.findChildren(QPushButton):
            if btn.text() == "Modifier":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'modifier' else "background-color: lightblue;")
            elif btn.text() == "Retirer":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'retirer' else "background-color: lightcoral;")

    def handle_button_click(self):
        if self.current_mode == 'modifier':
            self.vue.basculer_vers_ajout_succursale(False)
        elif self.current_mode == 'retirer':
            print("Mode Retirer activé.")
            ## retirer dans la base de données
        else:
            self.vue.afficher_message("Selectionner", "Veuillez sélectionner un mode")
