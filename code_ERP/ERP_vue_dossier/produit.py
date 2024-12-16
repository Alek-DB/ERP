from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QComboBox
from PySide6.QtCore import Signal
from ERP_data_base import DatabaseManager
import sqlite3

class AddModifyDialog(QDialog):
    def __init__(self, parent, mode="Ajouter", product_data=None):
        super().__init__()

        self.product_widget = parent
        self.mode = mode
        self.product_data = product_data

        self.setWindowTitle(self.mode)

        # Create the layout
        layout = QGridLayout()

        # Prendre le nom des colonnes dynamiquement
        labels = []
        try:
            db_manager = DatabaseManager('erp_database.db')
            # Obtenir les colonnes de la table Produits
            column_query = "PRAGMA table_info(Produits);"
            columns_info = db_manager.execute_query(column_query)
            labels = [column[1] for column in columns_info if column[1] != 'id_produit']

            # Obtenir les colonnes de la table Stocks
            column_query = "PRAGMA table_info(Stocks);"
            columns_info = db_manager.execute_query(column_query)
            stock_labels = [column[1] for column in columns_info if column[1] not in ('id_stock', 'id_produit', 'id_succursale')]

            labels.extend(stock_labels)
            labels.append('id_succursale')  # Ajouter le champ pour la succursale

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

        self.inputs = {}
        # Crée les labels selon les champs de la table
        for i, label in enumerate(labels):
            lbl = QLabel(label)

            if label == "id_succursale":
                # Créer un QComboBox pour le champ Succursale
                input_field = QComboBox()
                succursales = db_manager.execute_query("SELECT id_succursale, nom FROM Succursales")
                for succursale in succursales:
                    succursale_text = f"{succursale['id_succursale']}, {succursale['nom']}"
                    input_field.addItem(succursale_text)
            else:
                input_field = QLineEdit()

            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Désactiver le champ 'id_produit' si présent
        if 'id_produit' in self.inputs:
            self.inputs['id_produit'].setEnabled(False)

        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        # SI ON OUVRE LA CLASS EN MODE MODIFIER, ON DOIT REMPLIR LES CHAMPS AVEC LES VALEURS DE L'OBJECT À MODIFIER
        if self.mode == "Modifier" and self.product_data:
            self.fill_inputs()

        # SELON LE MODE, ON ENREGISTRE OU ON MODIFIE
        if self.mode == "Ajouter":
            self.add_modify_button.clicked.connect(self.enregistrer)
        else:
            self.add_modify_button.clicked.connect(self.modify_product)

    def fill_inputs(self):
        if self.product_data:
            for label in self.inputs.keys():
                value = self.product_data.get(label, '')
                if isinstance(self.inputs[label], QComboBox):
                    # Pour le champ 'id_succursale'
                    id_succursale = value
                    try:
                        db_manager = DatabaseManager('erp_database.db')
                        query = "SELECT nom FROM Succursales WHERE id_succursale = ?"
                        result = db_manager.execute_query(query, (id_succursale,))
                        if result:
                            nom_succursale = result[0]['nom']
                            succursale_text = f"{id_succursale}, {nom_succursale}"
                            self.inputs[label].setCurrentText(succursale_text)
                    except sqlite3.Error as e:
                        print(f"Erreur lors de la récupération de la succursale : {e}")
                else:
                    self.inputs[label].setText(str(value))

    def enregistrer(self):
        values = {}
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                selected_text = input_field.currentText()
                id_succursale = selected_text.split(",")[0]
                values[label] = int(id_succursale)
            else:
                values[label] = input_field.text()

        # Retirer 'id_produit' si présent
        values.pop('id_produit', None)

        # **Début de la validation des données**
        # Vérifier que les champs obligatoires sont remplis
        required_fields = ['nom_produit', 'prix', 'qte_actuelle', 'qte_max', 'qte_min_restock', 'id_succursale']
        for field in required_fields:
            if not values.get(field):
                QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
                return

        # Vérifier que les champs numériques contiennent des nombres valides
        try:
            values['prix'] = float(values['prix'])
            values['qte_actuelle'] = int(values['qte_actuelle'])
            values['qte_max'] = int(values['qte_max'])
            values['qte_min_restock'] = int(values['qte_min_restock'])
            values['id_succursale'] = int(values['id_succursale'])
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des nombres valides pour les champs numériques.")
            return
        # **Fin de la validation des données**

        try:
            db_manager = DatabaseManager('erp_database.db')

            # Insérer dans la table Produits
            produit_columns = ['nom_produit', 'code_produit', 'prix', 'description']
            produit_values = [values.get(col, None) for col in produit_columns]
            query_produit = f"""
            INSERT INTO Produits ({', '.join(produit_columns)})
            VALUES ({', '.join(['?'] * len(produit_columns))})
            """
            db_manager.execute_update(query_produit, produit_values)

            # Obtenir l'id_produit inséré
            id_produit = db_manager.cursor.lastrowid

            # Insérer dans la table Stocks
            stock_columns = ['id_produit', 'id_succursale', 'qte_actuelle', 'qte_max', 'qte_min_restock']
            stock_values = [
                id_produit,
                values.get('id_succursale'),
                values.get('qte_actuelle'),
                values.get('qte_max'),
                values.get('qte_min_restock')
            ]
            query_stock = f"""
            INSERT INTO Stocks ({', '.join(stock_columns)})
            VALUES ({', '.join(['?'] * len(stock_columns))})
            """
            db_manager.execute_update(query_stock, stock_values)

            print("Le produit a été ajouté avec succès.")
            self.product_widget.load_data()
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du produit : {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du produit : {e}")

        self.close()

    def modify_product(self):
        values = {}
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                selected_text = input_field.currentText()
                id_succursale = selected_text.split(",")[0]
                values[label] = int(id_succursale)
            else:
                values[label] = input_field.text()

        # **Début de la validation des données**
        # Vérifier que les champs obligatoires sont remplis
        required_fields = ['nom_produit', 'prix', 'qte_actuelle', 'qte_max', 'qte_min_restock', 'id_succursale']
        for field in required_fields:
            if not values.get(field):
                QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
                return

        # Vérifier que les champs numériques contiennent des nombres valides
        try:
            values['prix'] = float(values['prix'])
            values['qte_actuelle'] = int(values['qte_actuelle'])
            values['qte_max'] = int(values['qte_max'])
            values['qte_min_restock'] = int(values['qte_min_restock'])
            values['id_succursale'] = int(values['id_succursale'])
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des nombres valides pour les champs numériques.")
            return
        # **Fin de la validation des données**

        try:
            db_manager = DatabaseManager('erp_database.db')

            # Mettre à jour la table Produits
            produit_columns = ['nom_produit', 'code_produit', 'prix', 'description']
            produit_values = [values.get(col, None) for col in produit_columns]
            query_produit = f"""
            UPDATE Produits SET
            {', '.join([f"{col} = ?" for col in produit_columns])}
            WHERE id_produit = ?
            """
            db_manager.execute_update(query_produit, produit_values + [self.product_data['id_produit']])

            # Mettre à jour la table Stocks
            stock_columns = ['id_succursale', 'qte_actuelle', 'qte_max', 'qte_min_restock']
            stock_values = [
                values.get('id_succursale'),
                values.get('qte_actuelle'),
                values.get('qte_max'),
                values.get('qte_min_restock')
            ]
            query_stock = f"""
            UPDATE Stocks SET
            {', '.join([f"{col} = ?" for col in stock_columns])}
            WHERE id_produit = ?
            """
            db_manager.execute_update(query_stock, stock_values + [self.product_data['id_produit']])

            print("Le produit a été modifié avec succès.")
            self.product_widget.load_data()
        except sqlite3.Error as e:
            print(f"Erreur lors de la modification du produit : {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification du produit : {e}")

        self.close()

    def closeEvent(self, event):
        # Si vous avez besoin de réinitialiser des boutons ou des signaux dans votre widget parent
        pass



class QProduit(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__()

        self.parent = parent
        self.db_manager = db_manager

        # Create the main layout
        produit_layout = QGridLayout()

        # Left-side buttons layout
        add_button = QPushButton("Ajouter")
        remove_button = QPushButton("Retirer")
        modify_button = QPushButton("Modifier")
        back_button = QPushButton("<-")
        supplier_button = QPushButton("Fournisseur")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(modify_button)
        button_layout.addWidget(supplier_button)

        produit_layout.addLayout(button_layout, 0, 0)

        # Title of the inventory
        title_label = QLabel("Inventaire")
        title_label.setAlignment(Qt.AlignCenter)
        produit_layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_items)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        produit_layout.addLayout(search_layout, 1, 1)

        # Stock table
        self.produit_table = QTableWidget()
        self.produit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.produit_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.produit_table.setSelectionMode(QTableWidget.SingleSelection)
        self.produit_table.setColumnCount(7)
        self.produit_table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prix", "Description", "Max", "Quantité", "nb Restock"]
        )
        produit_layout.addWidget(self.produit_table, 2, 1)

        # Set layout
        self.setLayout(produit_layout)

        # Load data
        self.load_data()

        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)
        modify_button.clicked.connect(self.modify_item)
        back_button.clicked.connect(parent.basculer_before)

    def load_data(self):
        try:
            query = """
            SELECT p.*, s.qte_max, s.qte_actuelle, s.qte_min_restock
            FROM Produits p
            LEFT JOIN Stocks s ON p.id_produit = s.id_produit
            """
            results = self.db_manager.execute_query(query)
            self.produit_table.setRowCount(0)  # Clear existing data

            for row_number, row_data in enumerate(results):
                self.produit_table.insertRow(row_number)
                self.produit_table.setItem(row_number, 0, QTableWidgetItem(str(row_data['id_produit'])))
                self.produit_table.setItem(row_number, 1, QTableWidgetItem(row_data['nom_produit']))
                self.produit_table.setItem(row_number, 2, QTableWidgetItem(str(row_data['prix'])))
                self.produit_table.setItem(row_number, 3, QTableWidgetItem(str(row_data['description'])))
                self.produit_table.setItem(row_number, 4, QTableWidgetItem(str(row_data['qte_actuelle'])))
                self.produit_table.setItem(row_number, 5, QTableWidgetItem(str(row_data['qte_min_restock'])))
                

                # description = row_data['description'] or ''
                # self.produit_table.setItem(row_number, 3, QTableWidgetItem(description))

                # qte_max = row_data['qte_max'] if row_data['qte_max'] is not None else ''
                # self.produit_table.setItem(row_number, 4, QTableWidgetItem(str(qte_max)))

                # qte_actuelle = row_data['qte_actuelle'] if row_data['qte_actuelle'] is not None else ''
                # self.produit_table.setItem(row_number, 5, QTableWidgetItem(str(qte_actuelle)))

                # qte_min_restock = row_data['qte_min_restock'] if row_data['qte_min_restock'] is not None else ''
                # self.produit_table.setItem(row_number, 6, QTableWidgetItem(str(qte_min_restock)))

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des données : {e}")

    def add_item(self):
        dialog = AddModifyDialog(self, mode="Ajouter")
        dialog.exec_()


    def remove_item(self):
        selected_items = self.produit_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un produit à supprimer.")
            return

        # Supposons que la première colonne contient l'ID du produit
        row = selected_items[0].row()
        produit_id = self.produit_table.item(row, 0).text()

        # Demander confirmation
        reply = QMessageBox.question(self, 'Confirmation', 'Êtes-vous sûr de vouloir supprimer ce produit ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                # Supprimer le produit
                query = "DELETE FROM Produits WHERE id_produit = ?"
                parameters = (produit_id,)
                self.db_manager.execute_update(query, parameters)

                # Supprimer le stock associé
                query_stock = "DELETE FROM Stocks WHERE id_produit = ?"
                self.db_manager.execute_update(query_stock, parameters)

                # Mettre à jour l'affichage
                self.load_data()
                QMessageBox.information(self, "Succès", "Produit supprimé avec succès.")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la suppression : {e}")

    def modify_item(self):
        selected_items = self.produit_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un produit à modifier.")
            return

        row = selected_items[0].row()
        produit_id = self.produit_table.item(row, 0).text()

        # Récupérer les données actuelles du produit
        try:
            query = """
            SELECT p.*, s.qte_max, s.qte_actuelle, s.qte_min_restock, s.id_succursale
            FROM Produits p
            LEFT JOIN Stocks s ON p.id_produit = s.id_produit
            WHERE p.id_produit = ?
            """
            parameters = (produit_id,)
            result = self.db_manager.execute_query(query, parameters)
            if result:
                produit_data = dict(result[0])
            else:
                QMessageBox.warning(self, "Erreur", "Produit non trouvé.")
                return
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite : {e}")
            return

        # Ouvrir le dialogue avec les données existantes
        dialog = AddModifyDialog(self, mode="Modifier", product_data=produit_data)
        dialog.exec_()

    

    def search_items(self):
        search_text = self.search_input.text().lower()
        for row in range(self.produit_table.rowCount()):
            item = self.produit_table.item(row, 1)  # Nom du produit
            if search_text in item.text().lower():
                self.produit_table.setRowHidden(row, False)
            else:
                self.produit_table.setRowHidden(row, True)