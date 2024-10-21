from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from ERP_vue_dossier.employe_hr import EmployeHRWindow
from ERP_vue_dossier.commandes_hr import CommandesHRWindow

class qHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle("HR Management")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Titre
        title = QLabel("Gestion des Ressources Humaines")
        layout.addWidget(title)

        # Boutons pour naviguer
        button_layout = QHBoxLayout()

        employe_button = QPushButton("Employés")
        employe_button.clicked.connect(self.open_employe_hr)
        button_layout.addWidget(employe_button)

        commandes_button = QPushButton("Commandes")
        commandes_button.clicked.connect(self.open_commandes_hr)
        button_layout.addWidget(commandes_button)


        # Bouton Retour
        back_button = QPushButton("Back")
        back_button.clicked.connect(parent.basculer_vers_gerant_global)
        button_layout.addWidget(back_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_employe_hr(self):
        self.close()
        self.employe_window = EmployeHRWindow()
        self.employe_window.show()

    def open_commandes_hr(self):
        self.close()
        self.commandes_window = CommandesHRWindow()
        self.commandes_window.show()

    def go_back(self):
        self.close()
        from ERP_vue_dossier.hr import qHRWindow  # Import à l'intérieur de la fonction
        self.hr_window = qHRWindow()
        self.hr_window.show()
