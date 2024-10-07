from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

class QAddEmploye(QWidget):
    def __init__(self, parent=None):  # Add parent parameter
        super().__init__(parent)  # Pass the parent to the QWidget constructor
        
        self.setStyleSheet("QPushButton{padding: 10px; background-color:white; border:2px solid black;} "
                           "QPushButton:pressed{background-color:#cacccf;}")
        
        self.setWindowTitle("Ajouter un Employé")

        # Create input fields
        self.prenom_input = QLineEdit(self)
        self.nom_input = QLineEdit(self)
        self.poste_input = QLineEdit(self)
        self.salaire_input = QLineEdit(self)
        self.date_naissance_input = QLineEdit(self)
        self.date_embauche_input = QLineEdit(self)
        self.sexe_input = QLineEdit(self)
        self.statut_input = QLineEdit(self)
        self.allergies_input = QLineEdit(self)
        self.code_unique_input = QLineEdit(self)

        labels = ["Prénom", "Nom", "Poste", "Salaire", "Date de naissance", 
                  "Date d'embauche", "Sexe", "Statut", 
                  "Allergies/Préférences", "Code Unique"]
        input_widgets = [
            self.prenom_input, self.nom_input, self.poste_input, 
            self.salaire_input, self.date_naissance_input,
            self.date_embauche_input, self.sexe_input, 
            self.statut_input, self.allergies_input, 
            self.code_unique_input
        ]

        layout = QVBoxLayout()
        for label_text, input_widget in zip(labels, input_widgets):
            label = QLabel(label_text, self)
            layout.addWidget(label)
            layout.addWidget(input_widget)

        ajouter_button = QPushButton("Ajouter Employé", self)
        ajouter_button.clicked.connect(self.ajouter_employe)
        layout.addWidget(ajouter_button)

        self.setLayout(layout)

    def ajouter_employe(self):
        # The rest of the method remains unchanged...
        pass

    def clear_fields(self):
        # The rest of the method remains unchanged...
        pass
