from PySide6.QtWidgets import  QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

from ERP_emplacement import Emplacement


class QGerant(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        print(Emplacement.succursalesCode)
        
        self.setStyleSheet("QPushButton{padding: 10px; background-color:white; border:2px solid black;}  QPushButton:pressed{background-color:#cacccf;}")

        # Titre de la fenêtre
        self.setWindowTitle("Gérant")
        
        
        button1 = QPushButton("Stock")
        button2 = QPushButton("Finance")
        button3 = QPushButton("HR")
        button4 = QPushButton("Gérer employé")
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.addWidget(button4)
        
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        
        main_layout = QVBoxLayout()
        
        # Ajouter le bouton de retour en haut à droite
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)  # Bouton de retour
        back_layout.addStretch()  # Espaceur à gauche
        back_layout.setContentsMargins(0, 10, 10, 0)  # Marges autour du bouton de retour

        # Ajouter le layout du bouton de retour et le layout des boutons principaux
        main_layout.addLayout(back_layout)  # Ajouter le layout du bouton de retour
        main_layout.addLayout(button_layout)  # Ajouter le layout des boutons principaux

        # Appliquer le layout principal à la fenêtre
        self.setLayout(main_layout)