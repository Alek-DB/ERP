from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,QMessageBox
)
from ERP_role import Role

class QAddEmploye(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Employé")

        layout = QVBoxLayout()

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

        # Create role selection
        self.role_input = QComboBox(self)
        self.role_input.addItem("Administrateur", Role.ROLE_ADMINISTRATEUR)
        self.role_input.addItem("HR", Role.ROLE_HR)
        self.role_input.addItem("Gérant (Magasin)", Role.ROLE_GERANT)
        self.role_input.addItem("Commis", Role.ROLE_COMMIS)

        # Add input fields to layout
        layout.addWidget(QLabel("Prénom"))
        layout.addWidget(self.prenom_input)
        layout.addWidget(QLabel("Nom"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("Poste"))
        layout.addWidget(self.poste_input)
        layout.addWidget(QLabel("Salaire par heure"))
        layout.addWidget(self.salaire_input)
        layout.addWidget(QLabel("Date de naissance"))
        layout.addWidget(self.date_naissance_input)
        layout.addWidget(QLabel("Date d'embauche"))
        layout.addWidget(self.date_embauche_input)
        layout.addWidget(QLabel("Sexe"))
        layout.addWidget(self.sexe_input)
        layout.addWidget(QLabel("Statut"))
        layout.addWidget(self.statut_input)
        layout.addWidget(QLabel("Allergies/Préférences"))
        layout.addWidget(self.allergies_input)
        layout.addWidget(QLabel("Code Unique"))
        layout.addWidget(self.code_unique_input)
        
        # Add role selection to layout
        layout.addWidget(QLabel("Rôle"))
        layout.addWidget(self.role_input)

        ajouter_button = QPushButton("Ajouter Employé", self)
        ajouter_button.clicked.connect(self.ajouter_employe)
        layout.addWidget(ajouter_button)

        self.setLayout(layout)

    def ajouter_employe(self):
        # Get values from input fields
        employe_data = {
            'prenom': self.prenom_input.text(),
            'nom': self.nom_input.text(),
            'poste': self.poste_input.text(),
            'salaire': self.salaire_input.text(),
            'date_naissance': self.date_naissance_input.text(),
            'date_embauche': self.date_embauche_input.text(),
            'sexe': self.sexe_input.text(),
            'statut': self.statut_input.text(),
            'allergies_preferences_alimentaires': self.allergies_input.text(),
            'code_unique': self.code_unique_input.text(),
            'role': self.role_input.currentData()  # Get the selected role
        }

        # Now you can call the method to save this data to the database
        if self.controleur.ajouter_employe(employe_data):
            self.clear_fields()
            QMessageBox.information(self, "Succès", "Employé ajouté avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Échec de l'ajout de l'employé.")

    def clear_fields(self):
        self.prenom_input.clear()
        self.nom_input.clear()
        self.poste_input.clear()
        self.salaire_input.clear()
        self.date_naissance_input.clear()
        self.date_embauche_input.clear()
        self.sexe_input.clear()
        self.statut_input.clear()
        self.allergies_input.clear()
        self.code_unique_input.clear()
        self.role_input.setCurrentIndex(0)  # Reset to first role
