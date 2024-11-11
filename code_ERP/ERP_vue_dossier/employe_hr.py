from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
)
from ERP_vue_dossier.addModifyDialog import addModifyDialogEmploye
from employe.ERP_employeDAO import EmployeDAO


class EmployeHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Main layout for Employee interface
        main_layout = QVBoxLayout()

        # Search Box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Rechercher employé...")
        self.search_box.textChanged.connect(self.search_employee)
        search_button = QPushButton("Rechercher", self)
        search_button.clicked.connect(self.search_employee)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)


        # Labels for additional fields
        self.employee_code_label = QLabel("Code Employé:")
        self.hire_date_label = QLabel("Date d'Embauche:")
        self.position_label = QLabel("Position:")
        self.vacation_days_label = QLabel("Jours de Vacances Alloués:")

        # Table to display employee information
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(4)  # Adjust based on required columns
        self.employee_table.setHorizontalHeaderLabels([
            "Code Employé", "Nom", "Position", "Date d'Embauche"
        ])
        
        self.employee_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Permet de sélectionner une ligne complète
        self.employee_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Empêche l'édition dans la table

        # Connect table row selection
        self.employee_table.cellClicked.connect(self.on_employee_select)

        # Back button to return to the previous window
        back_button = QPushButton("Back")
        back_button.clicked.connect(parent.basculer_before)

        # Add widgets to the main layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.employee_code_label)
        main_layout.addWidget(self.hire_date_label)
        main_layout.addWidget(self.position_label)
        main_layout.addWidget(self.vacation_days_label)
        main_layout.addWidget(self.employee_table)
        main_layout.addWidget(back_button)  # Adding the back button at the end

        self.setLayout(main_layout)

    def search_employee(self):
        search_text = self.search_box.text().strip()
        filtered_employees = self.filter_employees(search_text)
        self.update_employee_display(filtered_employees)

    def filter_employees(self, search_text):
        employee_dao = EmployeDAO()  # Assuming you have an EmployeDAO class
        return employee_dao.get_employe_by_id(search_text)

    def update_employee_display(self, employees):
        self.employee_table.setRowCount(0)  # Clear previous results

        for employee in employees:
            row_position = self.employee_table.rowCount()
            self.employee_table.insertRow(row_position)
            self.employee_table.setItem(row_position, 0, QTableWidgetItem(employee['code_unique']))
            self.employee_table.setItem(row_position, 1, QTableWidgetItem(f"{employee['prenom']} {employee['nom']}"))
            self.employee_table.setItem(row_position, 2, QTableWidgetItem(employee['poste']))
            self.employee_table.setItem(row_position, 3, QTableWidgetItem(employee['date_embauche']))
            
    def on_employee_select(self, row, column):
    # Retrieve the employee code from the first column (Code Employé)
        code_employe = self.employee_table.item(row, 0).text()

        # Récupérer les données de l'employé en utilisant son code unique
        employee_dao = EmployeDAO()
        employee_data = employee_dao.get_employe_by_id(code_employe)

        if employee_data:
            # Si un employé est trouvé, ouvrir le dialogue de modification
            self.open_modify_dialog(employee_data)
        else:
            # Si aucun employé n'est trouvé, afficher un message d'erreur
            QMessageBox.warning(self, "Erreur", "Aucun employé trouvé avec ce code.")

    def open_modify_dialog(self, employee_data):
        """Open the dialog for modifying the employee."""
        dialog = addModifyDialogEmploye(self, mode="Modifier", product_data=employee_data)
        dialog.exec()