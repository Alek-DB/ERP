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

        self.vue = parent
        self.employee_dao = EmployeDAO()
        self.db_manager = DatabaseManager('erp_database.db')  # Make sure this line exists


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
        print(f"Code employé Update : {employees}")  # Ajouter cette ligne pour déboguer    

        if not employees:
            return

        for employee in employees:
            row_position = self.employee_table.rowCount()
            print(f"rowPos : {row_position}")
            self.employee_table.insertRow(row_position)
            self.employee_table.setItem(row_position, 0, QTableWidgetItem(str(employee.get('id_employe', 'N/A'))))
            self.employee_table.setItem(row_position, 1, QTableWidgetItem(f"{employee.get('prenom', '')}"))
            self.employee_table.setItem(row_position, 2, QTableWidgetItem(f"{employee.get('nom', '')}"))
            self.employee_table.setItem(row_position, 3, QTableWidgetItem(employee.get('poste', 'N/A')))
            self.employee_table.setItem(row_position, 4, QTableWidgetItem(employee.get('salaire', 'N/A')))
            self.employee_table.setItem(row_position, 5, QTableWidgetItem(employee.get('date_naissance', 'N/A')))
            self.employee_table.setItem(row_position, 6, QTableWidgetItem(employee.get('date_embauche', 'N/A')))
            self.employee_table.setItem(row_position, 7, QTableWidgetItem(employee.get('sexe', '')))
            self.employee_table.setItem(row_position, 8, QTableWidgetItem(employee.get('statut', 'N/A')))
            self.employee_table.setItem(row_position, 9, QTableWidgetItem(employee.get('allergies_preferences_alimentaires', 'N/A')))

    def open_modify_dialog(self, row):

        # Step 1: Retrieve the employee's ID from the selected row
        employee_id = self.employee_table.item(row, 0).text()  # Adjust column index if needed

        # Step 2: Query the database to fetch all employee details by ID
        query = "SELECT * FROM Employes WHERE id_employe = ?"
        result = self.db_manager.execute_query(query, (employee_id,))

        # Step 3: Prepare the employee data (convert tuple to a list for easier access)
        employee_data = []
        if result:
            employee_data = list(result[0])  # Convert the tuple into a list (same as you did for succursales)

        # Step 4: Open the modify dialog and pass the employee data
        if employee_data:
            dialog = AddModifyDialogEmploye(self, mode="Modifier", employee_data=employee_data)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Erreur", "Aucun employé trouvé avec cet ID.")

    
    def on_employee_select(self, row, column):
        """Triggered when an employee row is selected in the table."""
        # Retrieve the employee's unique ID from the first column (assuming first column holds unique identifier)
        code_employe = self.employee_table.item(row, 0).text()  # Adjust this if necessary (0 for 'id_employe')

        print(f"Code employé (on_employee_select): {code_employe}")  # Debugging line

        # Use EmployeDAO to fetch employee details by their unique ID
        employee_dao = EmployeDAO()
        employee_data = employee_dao.get_employe_by_id(code_employe)

        if employee_data:
            # If employee data is found, open the modification dialog
            self.open_modify_dialog(row)  # Pass the row index instead of employee data
        else:
            # Display an error message if no data is found
            QMessageBox.warning(self, "Erreur", "Aucun employé trouvé avec ce code.")


    def load_employee(self):
        try:
            db_manager = DatabaseManager('erp_database.db')
            # METTRE LE NOM DE VOTRE TABLE ET LES VALEURS A AFFICHER DANS LA LISTE
            query = "SELECT id_employe, prenom, nom, poste, salaire, date_naissance, date_embauche, sexe, statut, allergies_preferences_alimentaires FROM Employes"
            self.employee_table.setColumnCount(9) # METTRE LE MEME DE COLONNE
            rows = db_manager.execute_query(query, ())
            self.employee_table.setHorizontalHeaderLabels(["Id","Prenom", "Nom", "Poste", "Salaire", "Date de naissance", "Date d'embauche", "Sexe", "Allergies"])

            self.employee_table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.employee_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
            
            
    def fill_inputs(self):
        """Fill the inputs with the employee data in 'Modifier' mode."""
        if not self.employee_data:
            return  # No data to fill in

        # Assuming employee_data is a list, matching columns:
        labels = ["id_employe", "prenom", "nom", "poste", "salaire", "date_naissance", 
                "date_embauche", "sexe", "statut", "allergies_preferences_alimentaires", "username"]
        
        for label, value in zip(labels, self.employee_data):
            if label in self.inputs:
                input_field = self.inputs[label]
                if isinstance(input_field, QComboBox):
                    input_field.setCurrentText(str(value))
                else:
                    input_field.setText(str(value))

