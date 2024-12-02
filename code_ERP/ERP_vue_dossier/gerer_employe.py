import sys
import sqlite3
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel,
    QApplication, QMainWindow, QLineEdit, QTableWidget, QComboBox,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QMessageBox
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager
from ERP_emplacement import Emplacement

class AddModifyDialog(QDialog):
    def __init__(self, parent, mode="Ajouter", employee_data=None):
        super().__init__()

        self.gere_employe = parent
        self.mode = mode
        self.employee_data = employee_data

        self.setWindowTitle(self.mode)
        
        self.db_manager = DatabaseManager('erp_database.db')
        
        # Create the layout
        layout = QGridLayout()

        # Prendre le nom des colonnes dynamiquement
        labels = []
        try:
            column_query = "PRAGMA table_info(Employes);"
            columns_info = self.db_manager.execute_query(column_query)
            labels = [column[1] for column in columns_info if column[1] not in ("id_employe", "mot_de_passe")]
        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

        self.inputs = {}

        if Emplacement.succursalesId == -1 and self.mode == "Ajouter": #on est en gérant global    
            labels.append("Succursale")
        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "sex":
                # Créer un QComboBox pour le champ Sexe
                input_field = QComboBox()
                input_field.addItems(["M", "F"])  # Options du dropdown
            elif label == "Succursale":
                input_field = QComboBox()
                succursales = self.db_manager.execute_query("SELECT id_succursale, nom FROM Succursales")
                for succursale in succursales:
                    succursale_nom = f"{succursale[0]},  {succursale[1]}"
                    input_field.addItem(succursale_nom)
            else:
                input_field = QLineEdit()  # Champ texte pour les autres labels
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        self.inputs["date_naissance"].setPlaceholderText("YYYY-MM-DD")
        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        if self.mode == "Modifier" and self.employee_data:
            self.fill_inputs()

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        if self.mode == "Ajouter":
            self.add_modify_button.clicked.connect(self.enregistrer)
        else:
            self.add_modify_button.clicked.connect(self.modify_employee)
        
            
            
    def fill_inputs(self):
        if Emplacement.succursalesId == -1 and self.mode == "Ajouter": #on est en gérant global    
            succursale_employe = self.db_manager.execute_query("SELECT name FROM Succursales WHERE id_employe = ?", (self.employee_data[0],))
            self.employee_data.append(succursale_employe)
        if self.employee_data:
            for label, value in zip(self.inputs.keys(), self.employee_data):
                if isinstance(self.inputs[label], QComboBox):
                    self.inputs[label].setCurrentText(str(value))
                else:
                    self.inputs[label].setText(str(value))
            self.inputs['username'].setEnabled(False)  # Désactiver le champ ou ne pas l'afficher

    def modify_employee(self):
        values = [input_field.text() if not isinstance(input_field, QComboBox) else input_field.currentText() 
                for input_field in self.inputs.values()]
        
        if not all(values):
            print("Tous les champs doivent être remplis.")
            return

        self.gere_employe.update_employee(self.employee_data[9], values)  # Passer directement les valeurs
        self.close()

    def enregistrer(self):
        values = {label: input_field.currentText() if isinstance(input_field, QComboBox) else input_field.text() 
                  for label, input_field in self.inputs.items()}

        try:
            if Emplacement.succursalesId == -1 and self.mode == "Ajouter": #on est en gérant global    
                self.succursale = values.pop("Succursale")
            columns = ', '.join(values.keys())  # Clés du dictionnaire
            placeholders = ', '.join(['?'] * len(values))  # Des points d'interrogation pour les valeurs
            
            query = f"""
            INSERT INTO Employes ({columns})
            VALUES ({placeholders})
            """

            parameters = list(values.values())

            rows_affected = self.db_manager.execute_update(query, parameters)
            
            self.id = self.db_manager.cursor.lastrowid

            if rows_affected > 0:
                print("L'employé a été ajouté avec succès.")
                self.gere_employe.load_employe()
            else:
                print("Aucune ligne n'a été ajoutée.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
            return
            
        try:

            if Emplacement.succursalesId != -1: #on est en gérant global    
                self.succursale = Emplacement.succursalesId
                
            query = f"""
            INSERT INTO Employes_Succursales (id_employe, id_succursale, date_debut)
            VALUES ({self.id},{self.succursale}, date('now'))
            """
            
            print("Lien ----------------------------")
            print(query)
            print(self.db_manager.cursor.lastrowid)
            print(self.succursale)
            self.db_manager.execute_update(query, ())
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors du lien : {e}")



        try:
            
            values = (
                self.id, int(self.succursale),
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00",
                "09:00", "11:00"
            )

            query = """
                        INSERT INTO Horaires (id_employe, id_succursale, date,
                                            heure_entree_lundi, heure_sortie_lundi,
                                            heure_entree_mardi, heure_sortie_mardi,
                                            heure_entree_mercredi, heure_sortie_mercredi,
                                            heure_entree_jeudi, heure_sortie_jeudi,
                                            heure_entree_vendredi, heure_sortie_vendredi, statut)
                        VALUES (?, ?, date('now'),
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'actif')
                    """
            print("Horaire ----------------------------")
            print(query)
            print(values)
            self.db_manager.execute_update(query, values)
            print("horaire rajouter")
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de l'horaire: {e}")

        self.gere_employe.load_employe()
        self.close()

    def closeEvent(self, event):
        self.gere_employe.modify_button.setStyleSheet("background-color: ;")
        self.gere_employe.employe_table.itemClicked.disconnect()




class QGereEmploye(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.vue = parent
        self.db_manager = DatabaseManager('erp_database.db')

        # Create the main layout
        employe_layout = QGridLayout()

        # Left-side buttons layout (Ajouter, Retirer, Modifier, etc.)
        add_button = QPushButton("Ajouter")
        self.remove_button = QPushButton("Retirer")
        self.modify_button = QPushButton("Modifier")
        self.horaire_button = QPushButton("Horaire")
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.horaire_button)

        # Add button layout to the grid
        employe_layout.addLayout(button_layout, 0, 0)

        # Title of the employee management
        title_label = QLabel("Employés")
        title_label.setAlignment(Qt.AlignCenter)
        employe_layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        search_input = QLineEdit()

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        employe_layout.addLayout(search_layout, 1, 1)

        self.employe_table = QTableWidget()
        self.employe_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.employe_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employe_table.setSelectionMode(QTableWidget.SingleSelection)
        self.modify_item()
        self.employe_table.setColumnCount(5)  # Ajuster en fonction des colonnes d'employés
        self.setLayout(employe_layout)
        self.load_employe()

        # Add table to layout
        employe_layout.addWidget(self.employe_table, 2, 1)
        
        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.modify_button.clicked.connect(self.modify_item)
        self.horaire_button.clicked.connect(self.horaire_item)
        back_button.clicked.connect(self.vue.basculer_before)

    def load_employe(self):
        try:
            db_manager = DatabaseManager('erp_database.db')
            if Emplacement.succursalesId != -1:
                query = """
                SELECT e.id_employe, e.nom, e.username, e.sexe, e.poste
                FROM Employes e
                INNER JOIN Employes_Succursales es ON e.id_employe = es.id_employe
                WHERE es.id_succursale = ?
                """
                rows = db_manager.execute_query(query, (Emplacement.succursalesId,))
            else:
                query = "SELECT id_employe, nom, username, sexe, poste FROM Employes"
                rows = db_manager.execute_query(query, ())
                
            

            self.employe_table.setHorizontalHeaderLabels(["Id", "Nom", "Username", "Sexe", "Poste"])

            self.employe_table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.employe_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors du loading des employé : {e}")

    def add_item(self):
        dialog = AddModifyDialog(self)
        dialog.exec_()

    def remove_item(self):
        self.employe_table.itemClicked.disconnect()
        self.remove_button.setStyleSheet("background-color: lightCoral;")
        self.modify_button.setStyleSheet("background-color: ;")
        self.horaire_button.setStyleSheet("background-color: ;")
        self.employe_table.itemClicked.connect(self.confirm_deletion)

    def confirm_deletion(self, item):
        row = item.row()

        id_employe = self.employe_table.item(row, 0).text()

        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Confirmer la suppression")
        confirmation_dialog.setText(f"Voulez-vous vraiment supprimer l'employé '{id_employe}' ?")
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setIcon(QMessageBox.Warning)

        if confirmation_dialog.exec_() == QMessageBox.Yes:
            self.delete_employe(id_employe)
        else:
            self.employe_table.clearSelection()

        self.employe_table.itemClicked.disconnect()
        self.remove_button.setStyleSheet("background-color: ;")
        self.load_employe()

    def delete_employe(self, id_employe):
        try:
            db_manager = DatabaseManager('erp_database.db')
            
            result =  db_manager.execute_query("SELECT nom FROM Succursales WHERE gerant = ?", (id_employe,))
            print(result)
            if result: 
                QMessageBox.critical(None, "Erreur", f"L'employé est un gérant de la succursale {result[0][0]}")
                return
            
            db_manager.execute_query("DELETE FROM Employes_Roles WHERE id_employe = ?", (id_employe,))
            db_manager.execute_query("DELETE FROM Employes_Succursales WHERE id_employe = ?", (id_employe,))
            db_manager.execute_query("DELETE FROM Horaires WHERE id_employe = ?", (id_employe,))
            db_manager.execute_query("DELETE FROM Employes WHERE id_employe = ?", (id_employe,))

            print(f"L'employé {id_employe} a été supprimé.")
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Erreur", f"Une erreur est survenue lors de la supression : {e}")

    def modify_item(self):
        self.employe_table.itemClicked.disconnect()
        self.modify_button.setStyleSheet("background-color: lightgreen;")
        self.remove_button.setStyleSheet("background-color: ;")
        self.horaire_button.setStyleSheet("background-color: ;")
        self.employe_table.itemClicked.connect(self.open_modify_dialog)

    def open_modify_dialog(self, item):
        row = item.row()

        id_employe = self.employe_table.item(row, 0).text()  # Ajustez selon votre structure

        query = "SELECT * FROM Employes WHERE id_employe = ?"
        result = self.db_manager.execute_query(query, (id_employe,))

        employee_data = []
        if result:
            employee_data = list(result[0])  # Convertir le tuple en liste
            # Supprimer l'ID et le mot de passe
            employee_data.pop(0)  # Enlever l'ID
            employee_data.pop(9)  # Enlever le mot de passe

        dialog = AddModifyDialog(self, mode="Modifier", employee_data=employee_data)
        dialog.exec_()

    def update_employee(self, old_username_employe, new_values):
        try:
            column_query = "PRAGMA table_info(Employes);"
            columns_info = self.db_manager.execute_query(column_query)
            columns = [column[1] for column in columns_info if column[1] not in ('id_employe', 'mot_de_passe')]

            set_clause = ', '.join([f"{col} = ?" for col in columns])
            query = f"UPDATE Employes SET {set_clause} WHERE username = ?"

            values = new_values + [old_username_employe]

            self.db_manager.execute_update(query, values)

            self.load_employe()
            print(f"Employé mis à jour avec succès.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'employé: {e}")
            
    def horaire_item(self):
        self.employe_table.itemClicked.disconnect()
        self.modify_button.setStyleSheet("background-color: ;")
        self.remove_button.setStyleSheet("background-color: ;")
        self.horaire_button.setStyleSheet("background-color: lightYellow;")
        self.employe_table.itemClicked.connect(self.go_to)
    
    def go_to(self, item):
        self.vue.basculer_vers_horaire(self.employe_table.item(item.row(), 0).text())
