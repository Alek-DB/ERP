import sys
import sqlite3
from PySide6.QtWidgets import (

    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel,
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QComboBox,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog, QMessageBox

)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager



#POP UP PAGE POUR MODIFIER OU AJOUTER ITEM
class AddModifyDialog(QDialog):
    def __init__(self, parent, mode="Ajouter", product_data=None):
        super().__init__()

        self.succursale = parent
        self.mode = mode
        # Product data est un array des éléments qu'on veut afficher
        self.product_data = product_data

        self.setWindowTitle(self.mode)
        
        # Create the layout
        layout = QGridLayout()

        # Prendre le nom des colonnes dynamiquement
        labels = []
        try:
            db_manager = DatabaseManager('erp_database.db')
            column_query = "PRAGMA table_info(Succursales);"
            columns_info = db_manager.execute_query(column_query)
            # not in pour retirer ce qu'on ne veut pas demander ou modifier
            labels = [column[1] for column in columns_info]
            
        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

        self.inputs = {}
        # Crée les labels selon les champs de la table
        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "statut":
                # Créer un QComboBox pour le champ Statut
                input_field = QComboBox()
                input_field.addItems(["Actif", "Fermé"])  # Options du dropdown
            elif label == "gerant":
                input_field = QComboBox()
                gerants = db_manager.execute_query("SELECT id_employe, prenom, nom FROM Employes WHERE poste = 'Gérant'")
                for gérant in gerants:
                    gérant_nom = f"{gérant[0]}, {gérant[1]} {gérant[2]}"  # Prenom + Nom
                    input_field.addItem(gérant_nom)  # Ajouter le nom complet avec l'ID
            else:
                input_field = QLineEdit()  # Champ texte pour les autres labels
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        self.inputs['id_succursale'].setEnabled(False)  # Désactiver le champ ou ne pas l'afficher
    
        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        if self.mode == "Modifier" and self.product_data:
            self.fill_inputs()

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        if self.mode == "Ajouter":
            self.add_modify_button.clicked.connect(self.enregistrer)
        else:
            self.add_modify_button.clicked.connect(self.modify_product)
            
    def fill_inputs(self):
        """Quand on modifie, mettre les valeurs dans les champs."""
        if self.product_data:
            for label, value in zip(self.inputs.keys(), self.product_data):
                if isinstance(self.inputs[label], QComboBox):
                    if label == "gerant":
                        # Si le champ est "gerant", récupérer l'ID et remplir le QComboBox avec nom, prénom
                        gerant_id = value  # L'ID du gérant dans product_data
                        
                        try:
                            # Récupérer le prénom et le nom du gérant depuis la base de données
                            db_manager = DatabaseManager('erp_database.db')
                            query = "SELECT prenom, nom FROM Employes WHERE id_employe = ?"
                            result = db_manager.execute_query(query, (gerant_id,))
                            
                            if result:
                                prenom, nom = result[0]  # Extraire le prénom et le nom
                                # Ajouter l'ID et le nom/prénom au QComboBox
                                self.inputs[label].addItem(f"{gerant_id}, {prenom} {nom}")
                                # Définir l'élément sélectionné dans le QComboBox
                                self.inputs[label].setCurrentText(f"{gerant_id}, {prenom} {nom}")
                        except sqlite3.Error as e:
                            print(f"Erreur lors de la récupération du gérant : {e}")
                    else:
                        # Pour les autres QComboBox, on met simplement la valeur dans le champ
                        self.inputs[label].setCurrentText(str(value))
                else:
                    # Si ce n'est pas un QComboBox, c'est probablement un QLineEdit ou autre champ de texte
                    self.inputs[label].setText(str(value))

            # Désactiver le champ 'code' (comme dans votre code original)
            self.inputs['code'].setEnabled(False)


    def modify_product(self):
        # Récupérer les valeurs des champs de saisie
        values = []
        for input_field in self.inputs.values():
            if isinstance(input_field, QComboBox):
                # Si le champ est un QComboBox, et c'est le champ des gérants, on récupère seulement l'ID
                if input_field == self.inputs["gerant"]:  # Assurez-vous que vous avez bien le bon QComboBox
                    selected_text = input_field.currentText()
                    # Récupérer l'ID du gérant (avant la virgule)
                    gerant_id = selected_text.split(",")[0]
                    values.append(int(gerant_id))  # Ajouter l'ID du gérant
                else:
                    # Sinon, on récupère le texte complet du QComboBox
                    values.append(input_field.currentText())
            else:
                # Si c'est un QLineEdit, on récupère simplement le texte
                values.append(input_field.text())
        
        # Vérifier que tous les champs sont remplis
        if not all(values):
            print("Tous les champs doivent être remplis.")
            return

        # Appeler la méthode de la classe parente pour mettre à jour les données
        self.succursale.update_product(self.product_data[4], values)  # Passer directement les valeurs et le code
        self.close()

    def enregistrer(self):
        values = {}
            
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                # Si c'est un QComboBox et que c'est le champ "gerant", on extrait l'ID
                if label == "gerant":
                    selected_text = input_field.currentText()
                    # Extraire l'ID du gérant (avant la virgule)
                    gerant_id = selected_text.split(",")[0]
                    values[label] = int(gerant_id)  # Ajouter l'ID du gérant
                else:
                    # Sinon, on prend le texte complet du QComboBox
                    values[label] = input_field.currentText()
            else:
                # Si c'est un champ de type QLineEdit, on récupère le texte
                values[label] = input_field.text()

            # Retirer "id_succursale" si présent
            values.pop("id_succursale", None)

        try:
            db_manager = DatabaseManager('erp_database.db')

            # Construire la requête dynamiquement
            columns = ', '.join(values.keys())  # Clés du dictionnaire
            placeholders = ', '.join(['?'] * len(values))  # Des points d'interrogation pour les valeurs

            query = f"""
            INSERT INTO Succursales ({columns}, date_ouverture)
            VALUES ({placeholders}, date('now'))
            """

            # Récupérer les valeurs dans l'ordre des colonnes
            parameters = list(values.values())

            rows_affected = db_manager.execute_update(query, parameters)

            if rows_affected > 0:
                print("La succursale a été ajoutée avec succès.")
                self.succursale.load_succursale()
            else:
                print("Aucune ligne n'a été ajoutée.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de la créationd'une succursale : {e}")
            
            
            #CÉRATION LIEN EMPLOYÉ SUCCURSALE
        try:
            db_manager = DatabaseManager('erp_database.db')

            query = f"""
            INSERT INTO Employes_Succursales (id_employe, id_succursale, date_debut)
            VALUES ({values['gerant']},{db_manager.cursor.lastrowid }, date('now'))
            """
            
            print(query)
            db_manager.execute_update(query, ())
            
            print("lien créer")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

        self.close()

    def closeEvent(self, event):
        self.succursale.modify_button.setStyleSheet("background-color: ;")
        self.succursale.succursale_table.itemClicked.disconnect()

        
        
        
class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.vue = parent
        #set database
        self.db_manager = DatabaseManager('erp_database.db')

        # Create the main layout
        succursale_layout = QGridLayout()

        # Left-side buttons layout (Ajouter, Retirer, Modifier, etc.)
        add_button = QPushButton("Ajouter")
        self.remove_button = QPushButton("Retirer")
        self.modify_button = QPushButton("Modifier")
        self.open_button = QPushButton("Ouvrir")
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.open_button)

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
        self.succursale_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.succursale_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.succursale_table.setSelectionMode(QTableWidget.SingleSelection)
        self.modify_item()
        self.succursale_table.setColumnCount(8)
        self.setLayout(succursale_layout)
        self.load_succursale()

        # Add table to layout
        succursale_layout.addWidget(self.succursale_table, 2, 1)
        
        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.modify_button.clicked.connect(self.modify_item)
        self.open_button.clicked.connect(self.open_succursale)
        back_button.clicked.connect(self.vue.basculer_before)
             
    def load_succursale(self):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT id_succursale, nom, adresse, code, gerant, statut, telephone, date_ouverture FROM Succursales"
            rows = db_manager.execute_query(query, ())
            self.succursale_table.setHorizontalHeaderLabels(["Id","Nom", "Adresse", "Code", "Gerant", "Statut", "Telephone", "Date d'Ouverture"])

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
        self.succursale_table.itemClicked.disconnect()
        self.remove_button.setStyleSheet("background-color: lightCoral;")
        self.modify_button.setStyleSheet("background-color: ;")
        self.open_button.setStyleSheet("background-color: ;")
        self.succursale_table.itemClicked.connect(self.confirm_deletion)

    def confirm_deletion(self, item):
        """Demander confirmation avant de supprimer un élément."""
        # Obtenir la ligne de l'élément sélectionné
        row = item.row()

        nom_succursale = self.succursale_table.item(row, 1).text()
        id_succursale = self.succursale_table.item(row, 0).text()

        # Boîte de dialogue de confirmation
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Confirmer la suppression")
        confirmation_dialog.setText(f"Voulez-vous vraiment supprimer la succursale '{nom_succursale}' (Code: {id_succursale}) ?")
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setIcon(QMessageBox.Warning)

        # Si l'utilisateur confirme la suppression
        if confirmation_dialog.exec_() == QMessageBox.Yes:
            self.delete_succursale(id_succursale)
        else:
            # Annuler la sélection si l'utilisateur ne veut pas supprimer
            self.succursale_table.clearSelection()

        # Désactiver la connexion à l'événement après la suppression ou l'annulation
        self.succursale_table.itemClicked.disconnect()
        self.remove_button.setStyleSheet("background-color: ;")
        self.load_succursale()

    def delete_succursale(self, id_succursale):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "DELETE FROM Succursales WHERE id_succursale = ?"
            db_manager.execute_query(query, (id_succursale,))

            print(f"La succursale avec l'id {id_succursale} a été supprimé.")
        except Exception as e:
            print(f"Erreur lors de la suppression de la succursale: {e}") 

    def modify_item(self):
        self.succursale_table.itemClicked.disconnect()
        self.modify_button.setStyleSheet("background-color: lightgreen;")
        self.remove_button.setStyleSheet("background-color: ;")
        self.open_button.setStyleSheet("background-color: ;")
        self.succursale_table.itemClicked.connect(self.open_modify_dialog)
        
    def open_modify_dialog(self, item):
        row = item.row()

        succursale_id = self.succursale_table.item(row, 0).text()  # Ajustez selon votre structure

        # Étape 1: Sélectionner toutes les colonnes de la table
        query = "SELECT * FROM succursales WHERE id_succursale = ?"
        result = self.db_manager.execute_query(query, (succursale_id,))

        # Récupérer toutes les valeurs dans un tableau
        product_data = []
        if result:
            product_data = list(result[0])  # Convertir le tuple en liste

        # Ouvrir le dialogue en mode modification
        dialog = AddModifyDialog(self, mode="Modifier", product_data=product_data)
        dialog.exec_()
       
    def open_succursale(self):
        self.succursale_table.itemClicked.disconnect()
        self.open_button.setStyleSheet("background-color: lightblue;")
        self.remove_button.setStyleSheet("background-color: ;")
        self.modify_button.setStyleSheet("background-color: ;")
        self.succursale_table.itemClicked.connect(self.go_to)
        
    def go_to(self, item):
        self.vue.basculer_vers_gerant(self.succursale_table.item(item.row(), 0).text())

    def update_product(self, old_code_succursale, new_values):
        try:
            # Récupérer les noms des colonnes de la table sans l'ID
            column_query = "PRAGMA table_info(Succursales);"
            columns_info = self.db_manager.execute_query(column_query)
            columns = [column[1] for column in columns_info if column[1] not in ('id_succursale', 'date_ouverture')]

            # Construire la requête SQL dynamique
            set_clause = ', '.join([f"{col} = ?" for col in columns])
            query = f"UPDATE Succursales SET {set_clause} WHERE code = ?"

            # Combiner les nouvelles valeurs avec l'ancien code
            values = new_values + [old_code_succursale]

            # Impressions pour le débogage
            print("Requête SQL :", query)
            print("Valeurs à mettre à jour :", values)

            # Exécuter la mise à jour
            self.db_manager.execute_update(query, values)

            self.load_succursale()
            print(f"Succursale mise à jour avec succès.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la succursale: {e}")


