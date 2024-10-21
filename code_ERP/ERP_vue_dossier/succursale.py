import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QComboBox,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog, QMessageBox
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager


class AddModifyDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.succursale = parent
        
        #CREER UN EMPLOYÉ
        try:
            # Vérifier si la table est vide
            db_manager = DatabaseManager('erp_database.db')
            check_query = "SELECT COUNT(*) FROM Employes"
            result = db_manager.execute_query(check_query)
            count = result[0][0]  # Récupérer le nombre d'employés

            if count == 0:
                # Ajouter un nouvel employé
                insert_query = """
                INSERT INTO Employes (nom, prenom, poste) VALUES (?, ?, ?)
                """
                parameters = ("Dupont", "Jean", "Développeur")  # Remplacez par les valeurs souhaitées
                rows_affected = db_manager.execute_update(insert_query, parameters)


                if rows_affected > 0:
                    print("Un nouvel employé a été ajouté avec succès.")
                else:
                    print("Aucun employé n'a été ajouté.")
            else:
                print("La table n'est pas vide. Aucun employé n'a été ajouté.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {type(e).__name__} - {e}")
        
 
        self.setWindowTitle("Ajouter")
        # Create the layout
        layout = QGridLayout()

        # prend le nom des tables
        labels = []
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT * FROM Succursales"
            db_manager.execute_query(query, ())
            labels = db_manager.get_column_names()
            labels.remove("date_ouverture")
            labels.remove("id_succursale")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
            
        self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "statut":
                # Créer un QComboBox pour le champ Statut
                input_field = QComboBox()
                input_field.addItems(["Actif", "Fermé"])  # Options du dropdown
            else:
                input_field = QLineEdit()  # Champ texte pour les autres labels
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton("Ajouter")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        self.add_modify_button.clicked.connect(self.enregistrer)
        
        
    def enregistrer(self):
        """Récupérer les valeurs des champs et les enregistrer dans la base de données."""
        values = {
            label: input_field.currentText() if isinstance(input_field, QComboBox) else input_field.text() 
            for label, input_field in self.inputs.items()
        }

        try: 
            db_manager = DatabaseManager('erp_database.db')
            
            # Construire la requête dynamiquement
            columns = ', '.join(values.keys())  # Clés du dictionnaire
            placeholders = ', '.join(['?'] * (len(values)))  # Des points d'interrogation pour les valeurs


            query = f"""
            INSERT INTO Succursales ({columns}, date_ouverture)
            VALUES ({placeholders}, date('now'))
            """

            # Récupérer les valeurs dans l'ordre des colonnes
            parameters = list(values.values()) 

            rows_affected = db_manager.execute_update(query, parameters)

            if rows_affected > 0:
                print("La succursale a été ajouté avec succès.")
                self.succursale.load_succursale()
            else:
                print("Aucune ligne n'a été ajoutée.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
        
        self.close()
        
        
        
class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        #set database
        self.db_manager = DatabaseManager('erp_database.db')

        # Create the main layout
        succursale_layout = QGridLayout()

        # Left-side buttons layout (Ajouter, Retirer, Modifier, etc.)
        add_button = QPushButton("Ajouter")
        remove_button = QPushButton("Retirer")
        modify_button = QPushButton("Modifier")
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(modify_button)

        # Add button layout to the grid
        succursale_layout.addLayout(button_layout, 0, 0)

        # Title of the inventory
        title_label = QLabel("Succursales")
        title_label.setAlignment(Qt.AlignCenter)
        succursale_layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        search_input = QLineEdit()

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        succursale_layout.addLayout(search_layout, 1, 1)

        self.succursale_table = QTableWidget()
        self.succursale_table.setColumnCount(7)
        self.setLayout(succursale_layout)
        self.load_succursale()

        # Add table to layout
        succursale_layout.addWidget(self.succursale_table, 2, 1)

        # Set central widget
    

        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)
        modify_button.clicked.connect(self.modify_item)
        back_button.clicked.connect(parent.basculer_vers_gerant_global)
             
    def load_succursale(self):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT nom, adresse, code, gerant, statut, telephone, date_ouverture FROM Succursales"
            rows = db_manager.execute_query(query, ())
            self.succursale_table.setHorizontalHeaderLabels(["Nom", "Adresse", "Code", "Gerant", "Statut", "Telephone", "Date d'Ouverture"])

            self.succursale_table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.succursale_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

    def add_item(self):
        # Open the Add/Modify dialog
        dialog = AddModifyDialog(self)
        dialog.exec_()
        
    def remove_item(self):
        # Activer la sélection dans le tableau
        self.succursale_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.succursale_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Connecter l'événement de clic à la méthode `confirm_deletion`
        self.succursale_table.itemClicked.connect(self.confirm_deletion)

    def confirm_deletion(self, item):
        """Demander confirmation avant de supprimer un élément."""
        # Obtenir la ligne de l'élément sélectionné
        row = item.row()

        nom_succursale = self.succursale_table.item(row, 0).text()
        code_succursale = self.succursale_table.item(row, 2).text()

        # Boîte de dialogue de confirmation
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Confirmer la suppression")
        confirmation_dialog.setText(f"Voulez-vous vraiment supprimer la succursale '{nom_succursale}' (Code: {code_succursale}) ?")
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setIcon(QMessageBox.Warning)

        # Si l'utilisateur confirme la suppression
        if confirmation_dialog.exec_() == QMessageBox.Yes:
            self.delete_succursale(code_succursale)
        else:
            # Annuler la sélection si l'utilisateur ne veut pas supprimer
            self.succursale_table.clearSelection()

        # Désactiver la connexion à l'événement après la suppression ou l'annulation
        self.succursale_table.itemClicked.disconnect()
        self.load_succursale()

    def delete_succursale(self, code_succursale):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "DELETE FROM Succursales WHERE code = ?"
            db_manager.execute_query(query, (code_succursale,))

            # Message de confirmation
            print(f"La succursale avec le code {code_succursale} a été supprimé.")
        except Exception as e:
            print(f"Erreur lors de la suppression de la succursale: {e}") 

    def modify_item(self):
        # Code to modify the selected item in the stock
        print("Modify item clicked")
        # Add logic to modify the selected row
        

