import sqlite3
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QDialog,
    QLabel, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
)
from ERP_vue_dossier.addModifyDialog import addModifyDialogEmploye
from ERP_employeDAO import EmployeDAO
from ERP_data_base import DatabaseManager

class AddModifyDialogEmploye(QDialog):
    def __init__(self, parent, mode="Ajouter", employee_data=None):
        super().__init__()

        self.parent = parent
        self.mode = mode
        self.employee_data = employee_data

        self.setWindowTitle(f"{mode} Employé")

        layout = QGridLayout()

        labels = []
        try:
            db_manager = DatabaseManager('erp_database.db')
            column_query = "PRAGMA table_info(Employes);"
            columns_info = db_manager.execute_query(column_query)
            labels = [column[1] for column in columns_info]
        except sqlite3.Error as e:
            print(f"Erreur: {e}")

        self.inputs = {}
        for i, label in enumerate(labels):
            lbl = QLabel(label)

            if label == "poste":
                input_field = QComboBox()
                input_field.addItems(["Manager", "Technicien", "Admin", "Employé"])
            elif label == "statut":
                input_field = QComboBox()
                input_field.addItems(["Actif", "Inactif"])
            elif label == "sexe":
                input_field = QComboBox()
                input_field.addItems(["Homme", "Femme", "Autre"])
            elif label == "date_naissance" or label == "date_embauche":
                input_field = QLineEdit()
                input_field.setPlaceholderText("AAAA-MM-JJ")  #
            else:
                input_field = QLineEdit()

            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Disable champ ID si on est dans "Modifier"
        if mode == "Modifier" and "id_employe" in self.inputs:
            self.inputs["id_employe"].setEnabled(False)


        self.save_button = QPushButton(mode)
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)
        self.setLayout(layout)


        if mode == "Modifier" and employee_data:
            self.fill_inputs()

        # Vincular el botón de guardar según el modo
        self.save_button.clicked.connect(self.save_employee)

    def fill_inputs(self):
        """Llena los campos con datos del empleado en modo 'Modifier'."""
        for label, value in zip(self.inputs.keys(), self.employee_data):
            if isinstance(self.inputs[label], QComboBox):
                self.inputs[label].setCurrentText(str(value))
            else:
                self.inputs[label].setText(str(value))

    def save_employee(self):
        """Guardar o modificar datos del empleado."""
        values = {}
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                values[label] = input_field.currentText()
            else:
                values[label] = input_field.text()

        if not all(values.values()):
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        db_manager = DatabaseManager('erp_database.db')
        try:
            if self.mode == "Ajouter":

                columns = ', '.join(values.keys())
                placeholders = ', '.join(['?'] * len(values))
                query = f"INSERT INTO Employes ({columns}) VALUES ({placeholders})"
                db_manager.execute_update(query, list(values.values()))
                QMessageBox.information(self, "Succès", "Employé ajouté avec succès.")
            else:

                updates = ', '.join([f"{col} = ?" for col in values.keys()])
                query = f"UPDATE Employes SET {updates} WHERE id_employe = ?"
                db_manager.execute_update(query, list(values.values()) + [self.employee_data[0]])
                QMessageBox.information(self, "Succès", "Employé modifié avec succès.")

            self.parent.refresh_employees()  # Mis à jour liste
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")
            

class EmployeHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.employee_dao = EmployeDAO()

        # Main layout
        main_layout = QVBoxLayout()

        # Search box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Rechercher employé...")
        self.search_box.textChanged.connect(self.search_employee)

        search_button = QPushButton("Rechercher", self)
        search_button.clicked.connect(self.search_employee)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)

        # Table to display employee information
        self.employee_table = QTableWidget()

        # Obtener todas las columnas dinámicamente
        column_names = self.employee_dao.get_column_names()
        self.employee_table.setColumnCount(len(column_names))
        self.employee_table.setHorizontalHeaderLabels(column_names)
        self.employee_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.employee_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Mod employe
        self.employee_table.cellClicked.connect(self.on_employee_select)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(parent.basculer_before)

        # Add widgets to layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.employee_table)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)


    def search_employee(self):
        """Search and display employees matching the search text."""
        search_text = self.search_box.text().strip()
        employees = EmployeDAO().get_employe_by_id(search_text)
        self.update_employee_display(employees)

    def update_employee_display(self, employees):
        
        self.employee_table.setRowCount(0)  # Clear previous results

        if not employees:
            return

        for employee in employees:
            row_position = self.employee_table.rowCount()
            self.employee_table.insertRow(row_position)
            self.employee_table.setItem(row_position, 0, QTableWidgetItem(employee.get('code_unique', 'N/A')))
            self.employee_table.setItem(row_position, 1, QTableWidgetItem(f"{employee.get('prenom', '')} {employee.get('nom', '')}"))
            self.employee_table.setItem(row_position, 2, QTableWidgetItem(employee.get('poste', 'N/A')))
            self.employee_table.setItem(row_position, 3, QTableWidgetItem(employee.get('date_embauche', 'N/A')))


    def open_modify_dialog(self, employee_data):
        """Open the dialog for modifying the employee."""
        dialog = addModifyDialogEmploye(self, mode="Modifier", employee_data=employee_data)  # Corrected here
        dialog.exec()
    
    def on_employee_select(self, row):
        """Triggered when an employee row is selected in the table."""
        # Retrieve the employee's unique code from the first column (assumes first column holds unique identifier)
        code_employe = self.employee_table.item(row, 0).text()

        # Use EmployeDAO to fetch employee details by their unique code
        employee_dao = EmployeDAO()
        employee_data = employee_dao.get_employe_by_id(code_employe)

        if employee_data:
            # If employee data is found, open the modification dialog
            self.open_modify_dialog(employee_data)
        else:
            # Display error message if no data is found
            QMessageBox.warning(self, "Erreur", "Aucun employé trouvé avec ce code.")


