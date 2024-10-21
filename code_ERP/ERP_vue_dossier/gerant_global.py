from PySide6.QtWidgets import  QWidget, QPushButton, QHBoxLayout
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
        button3 = QPushButton("Règle d'affaire")
        button4 = QPushButton("HR")
        button4.clicked.connect(parent.basculer_vers_hr)

        # Mise en page horizontale
        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        

        # Ajouter du padding entre les boutons
        layout.setSpacing(30)  # Espacement entre les boutons
        layout.setContentsMargins(50, 50, 50, 50)  # Marges de la mise en page

        # Centrer le layout dans la fenêtre
        layout.setAlignment(Qt.AlignCenter)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout)