from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

from ERP_employeDAO import EmployeDAO

class addModifyDialogEmploye(QDialog):
    def __init__(self, parent, mode="Ajouter", employee_data=None):
        super().__init__(parent)

        self.mode = mode
        self.employee_data = employee_data
        
        self.setWindowTitle(f"{mode} Employé")

        # Layout principal
        layout = QVBoxLayout()

        # Formulaire pour les informations de l'employé
        form_layout = QFormLayout()

        # Champs de formulaire pour les informations de l'employé
        self.prenom_input = QLineEdit(self)
        self.nom_input = QLineEdit(self)
        self.poste_input = QLineEdit(self)
        self.salaire_input = QLineEdit(self)

        # Si en mode modification, pré-remplir les champs avec les données existantes
        if self.mode == "Modifier" and self.employee_data:
            self.prenom_input.setText(self.employee_data['prenom'])
            self.nom_input.setText(self.employee_data['nom'])
            self.poste_input.setText(self.employee_data['poste'])
            self.salaire_input.setText(str(self.employee_data['salaire']))

        # Ajout des champs au formulaire
        form_layout.addRow("Prénom", self.prenom_input)
        form_layout.addRow("Nom", self.nom_input)
        form_layout.addRow("Poste", self.poste_input)
        form_layout.addRow("Salaire", self.salaire_input)

        layout.addLayout(form_layout)

        # Boutons de validation
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Enregistrer", self)
        self.cancel_button = QPushButton("Annuler", self)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        # Connexions des boutons
        self.save_button.clicked.connect(self.save_employee)
        self.cancel_button.clicked.connect(self.reject)  # Fermer la fenêtre sans rien enregistrer

        self.setLayout(layout)

    def save_employee(self):
        # Récupérer les valeurs des champs et mettre à jour les données dans la base
        prenom = self.prenom_input.text()
        nom = self.nom_input.text()
        poste = self.poste_input.text()
        salaire = self.salaire_input.text()

        if not (prenom and nom and poste and salaire):
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        # Appel à la méthode de mise à jour dans la base de données
        employee_dao = EmployeDAO()
        if self.mode == "Modifier":
            employee_dao.update_employe(self.employee_data['id_employe'], prenom, nom, poste, salaire)

        self.accept()  # Fermer la fenêtre et valider l'opération
