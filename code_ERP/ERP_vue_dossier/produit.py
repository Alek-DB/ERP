from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QComboBox
from PySide6.QtCore import Signal

class AddModifyDialog(QDialog):
    item_added = Signal(dict)

    def __init__(self, db_manager, mode="Ajouter", produit_data=None):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle(f"{mode} Produit")

        # Create the layout
        layout = QGridLayout()

        # Labels and input fields
        labels = ["Nom", "Prix", "Description", "Max", "Quantité", "nb Restock", "Succursale"]
        self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "Succursale":
                input_field = QComboBox()
                # Récupérer la liste des succursales depuis la base de données
                succursales = self.get_succursales()
                input_field.addItems(succursales)
            else:
                input_field = QLineEdit()
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton(mode)
        self.cancel_button = QPushButton("Annuler")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)

        # Connect add/modify button to confirm_add method
        self.add_modify_button.clicked.connect(self.confirm_add)

        # Si nous sommes en mode "Modifier", pré-remplir les champs
        if produit_data:
            self.fill_fields(produit_data)

    def get_succursales(self):
        try:
            query = "SELECT id_succursale, nom FROM Succursales"
            results = self.db_manager.execute_query(query)
            # Créer une liste avec des chaînes "id_succursale - nom"
            succursales = [f"{row['id_succursale']} - {row['nom']}" for row in results]
            return succursales
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de récupérer les succursales : {e}")
            return []

    def confirm_add(self):
        data = {}
        for label, input_field in self.inputs.items():
            if label == "Succursale":
                succursale_text = input_field.currentText()
                if succursale_text:
                    id_succursale = succursale_text.split(" - ")[0]
                    data[label] = id_succursale
                else:
                    data[label] = None
            else:
                data[label] = input_field.text()
        self.item_added.emit(data)
        self.close()


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
        back_button.clicked.connect(parent.basculer_vers_splash)

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

                description = row_data['description'] or ''
                self.produit_table.setItem(row_number, 3, QTableWidgetItem(description))

                qte_max = row_data['qte_max'] if row_data['qte_max'] is not None else ''
                self.produit_table.setItem(row_number, 4, QTableWidgetItem(str(qte_max)))

                qte_actuelle = row_data['qte_actuelle'] if row_data['qte_actuelle'] is not None else ''
                self.produit_table.setItem(row_number, 5, QTableWidgetItem(str(qte_actuelle)))

                qte_min_restock = row_data['qte_min_restock'] if row_data['qte_min_restock'] is not None else ''
                self.produit_table.setItem(row_number, 6, QTableWidgetItem(str(qte_min_restock)))

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des données : {e}")

    def add_item(self):
        # Open the Add/Modify dialog
        dialog = AddModifyDialog(self.db_manager, mode="Ajouter")
        dialog.item_added.connect(self.insert_item_into_db)
        dialog.exec_()

    def insert_item_into_db(self, data):
        # Validation des données
        required_fields = ['Nom', 'Prix', 'Max', 'Quantité', 'nb Restock', 'Succursale']
        for field in required_fields:
            if not data[field]:
                QMessageBox.warning(self, "Attention", f"Le champ {field} est obligatoire.")
                return

        try:
            prix = float(data['Prix'])
            qte_max = int(data['Max'])
            quantite = int(data['Quantité'])
            qte_restock = int(data['nb Restock'])
            id_succursale = int(data['Succursale'])
        except ValueError:
            QMessageBox.warning(self, "Attention", "Veuillez entrer des nombres valides pour Prix, Max, Quantité, nb Restock, et sélectionner une succursale.")
            return

        # Insérer les données dans la base de données
        try:
            query = """
            INSERT INTO Produits (nom_produit, prix, description)
            VALUES (?, ?, ?)
            """
            parameters = (
                data['Nom'],
                prix,
                data.get('Description', '')
            )
            self.db_manager.execute_update(query, parameters)

            # Récupérer l'id_produit inséré
            result = self.db_manager.execute_query("SELECT last_insert_rowid() as id_produit")
            id_produit = result[0]['id_produit']

            # Insérer les quantités dans la table Stocks
            query_stock = """
            INSERT INTO Stocks (id_produit, id_succursale, qte_max, qte_actuelle, qte_min_restock)
            VALUES (?, ?, ?, ?, ?)
            """
            parameters_stock = (
                id_produit,
                id_succursale,
                qte_max,
                quantite,
                qte_restock
            )
            self.db_manager.execute_update(query_stock, parameters_stock)

            # Mettre à jour l'affichage
            self.load_data()
            QMessageBox.information(self, "Succès", "Produit ajouté avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de l'ajout : {e}")


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
            SELECT p.*, s.qte_max, s.qte_actuelle, s.qte_min_restock
            FROM Produits p
            LEFT JOIN Stocks s ON p.id_produit = s.id_produit
            WHERE p.id_produit = ?
            """
            parameters = (produit_id,)
            result = self.db_manager.execute_query(query, parameters)
            if result:
                produit_data = result[0]
            else:
                QMessageBox.warning(self, "Erreur", "Produit non trouvé.")
                return
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite : {e}")
            return

        # Ouvrir le dialogue avec les données existantes
        dialog = AddModifyDialog(self.db_manager, mode="Modifier", produit_data=produit_data)
        dialog.item_added.connect(lambda data: self.update_item_in_db(produit_id, data))
        dialog.exec_()

    def update_item_in_db(self, produit_id, data):
        # Validation des données
        required_fields = ['Nom', 'Prix', 'Max', 'Quantité', 'nb Restock']
        for field in required_fields:
            if not data[field]:
                QMessageBox.warning(self, "Attention", f"Le champ {field} est obligatoire.")
                return

        try:
            prix = float(data['Prix'])
            qte_max = int(data['Max'])
            quantite = int(data['Quantité'])
            qte_restock = int(data['nb Restock'])
        except ValueError:
            QMessageBox.warning(self, "Attention", "Veuillez entrer des nombres valides pour Prix, Max, Quantité et nb Restock.")
            return

        # Mettre à jour les données dans la base de données
        try:
            query = """
            UPDATE Produits SET nom_produit = ?, prix = ?, description = ?
            WHERE id_produit = ?
            """
            parameters = (
                data['Nom'],
                prix,
                data.get('Description', ''),
                produit_id
            )
            self.db_manager.execute_update(query, parameters)

            # Mettre à jour les quantités dans la table Stocks
            query_stock = """
            UPDATE Stocks SET qte_max = ?, qte_actuelle = ?, qte_min_restock = ?
            WHERE id_produit = ?
            """
            parameters_stock = (
                qte_max,
                quantite,
                qte_restock,
                produit_id
            )
            self.db_manager.execute_update(query_stock, parameters_stock)

            # Mettre à jour l'affichage
            self.load_data()
            QMessageBox.information(self, "Succès", "Produit modifié avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la modification : {e}")

    def search_items(self):
        search_text = self.search_input.text().lower()
        for row in range(self.produit_table.rowCount()):
            item = self.produit_table.item(row, 1)  # Nom du produit
            if search_text in item.text().lower():
                self.produit_table.setRowHidden(row, False)
            else:
                self.produit_table.setRowHidden(row, True)