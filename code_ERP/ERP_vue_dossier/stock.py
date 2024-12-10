import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager


class AddModifyDialog(QDialog):
    def __init__(self, parent=None, mode="Ajouter", product_data=None):
        """
        Initialise le dialogue pour ajouter ou modifier un produit.

        :param parent: La fenêtre parente
        :param mode: "Ajouter" ou "Modifier" pour déterminer le comportement du dialogue
        :param product_data: Les données du produit à modifier (None si on ajoute un produit)
        """
        super().__init__(parent)
        self.mode = mode
        self.product_data = product_data
        self.setWindowTitle(self.mode)

        # Create the layout
        layout = QGridLayout()

        # Labels et champs de saisie
        if self.mode == "Ajouter":
            labels = ["Max", "Quantité", "nb Restock"]
            self.inputs = {}
            
            # Ajout d'un QComboBox pour sélectionner un produit
            self.product_combobox = QComboBox()
            self.populate_product_combobox()  # Remplir le QComboBox avec les produits existants
            layout.addWidget(QLabel("Sélectionner un produit"), 0, 0)
            layout.addWidget(self.product_combobox, 0, 1)
        else:
            labels = ["Max", "Quantité", "nb Restock"]
            self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            input_field = QLineEdit()
            layout.addWidget(lbl, i + 1, 0)  # décaler les champs pour l'affichage
            layout.addWidget(input_field, i + 1, 1)
            self.inputs[label] = input_field

        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels) + 1, 1)

        # Set the layout
        self.setLayout(layout)

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)

        # Pre-fill the inputs if in modify mode
        if self.mode == "Modifier" and self.product_data:
            self.fill_inputs()

        # Connect add/modify button to the appropriate method
        if self.mode == "Ajouter":
            self.add_button.clicked.connect(self.add_product)
        else:
            self.add_button.clicked.connect(self.modify_product)

    def populate_product_combobox(self):
        """Remplir le QComboBox avec les produits existants dans la base de données."""
        query = "SELECT code_produit, nom_produit FROM Produits"
        rows = self.parent().conn.execute_query(query)
        
        for row in rows:
            self.product_combobox.addItem(f"{row['code_produit']} - {row['nom_produit']}", row['code_produit'])

    def fill_inputs(self):
        """Pré-remplir les champs avec les données du produit existant pour la modification."""
        if self.product_data:
            self.inputs["Max"].setText(str(self.product_data['qte_max']))
            self.inputs["Quantité"].setText(str(self.product_data['qte_actuelle']))
            self.inputs["nb Restock"].setText(str(self.product_data['qte_min_restock']))

    def add_product(self):
        """Valider les champs et ajouter le produit dans la base de données."""
        # Récupérer le code du produit sélectionné dans le QComboBox
        selected_code = self.product_combobox.currentData()
        
        # Vérifier que le produit est sélectionné
        if not selected_code:
            print("Veuillez sélectionner un produit.")
            return

        # Récupérer les valeurs des champs de saisie
        qte_max = self.inputs["Max"].text()
        qte_actuelle = self.inputs["Quantité"].text()
        restock = self.inputs["nb Restock"].text()

        # Vérifier que tous les champs sont remplis
        if not (qte_max and qte_actuelle and restock):
            print("Tous les champs doivent être remplis.")
            return

        # Vérifier que les valeurs numériques sont valides
        try:
            qte_max = int(qte_max)
            qte_actuelle = int(qte_actuelle)
            restock = int(restock)
        except ValueError:
            QMessageBox.critical(None, "Erreur", f"Quantité, Restock et Prix doivent être des nombres valides")
            print("Erreur : Quantité, Restock et Prix doivent être des nombres valides.")
            return

        # Appeler la méthode de la classe parente pour insérer les données dans Stocks
        self.parent().add_new_product(selected_code, qte_max, qte_actuelle, restock)
        self.close()

    def modify_product(self):
        """Valider les champs et modifier le produit dans la base de données."""
        # Récupérer le code du produit sélectionné dans le QComboBox
        selected_code = self.product_data['code_produit']

        # Récupérer les valeurs des champs de saisie
        qte_max = self.inputs["Max"].text()
        qte_actuelle = self.inputs["Quantité"].text()
        restock = self.inputs["nb Restock"].text()

        # Vérifier que tous les champs sont remplis
        if not (qte_max and qte_actuelle and restock):
            print("Tous les champs doivent être remplis.")
            return

        # Vérifier que les valeurs numériques sont valides
        try:
            qte_max = int(qte_max)
            qte_actuelle = int(qte_actuelle)
            restock = int(restock)
        except ValueError:
            QMessageBox.critical(None, "Erreur", f"Quantité, Restock et Prix doivent être des nombres valides")
            print("Erreur : Quantité, Restock et Prix doivent être des nombres valides.")
            return

        # Appeler la méthode de la classe parente pour mettre à jour le produit dans Stocks
        self.parent().update_product(selected_code, qte_max, qte_actuelle, restock)
        self.close()

        
    
        
        
class QStock(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        #set database
        self.conn = DatabaseManager('erp_database.db')
        #self.cursor = self.conn.cursor()

        # Create the main layout
        stock_layout = QGridLayout()

        # Left-side buttons layout (Ajouter, Retirer, Modifier, etc.)
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

        # Add button layout to the grid
        stock_layout.addLayout(button_layout, 0, 0)

        # Title of the inventory
        title_label = QLabel("Inventaire")
        title_label.setAlignment(Qt.AlignCenter)
        stock_layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        search_input = QLineEdit()

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        stock_layout.addLayout(search_layout, 1, 1)

        # Stock table (Liste, max, qte, restock, prix)
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels(
            ["Nom", "Code Produit", "Max", "Quantité", "Restock", "Prix"]
        )
        
        self.load_stock_data()
        
        # Dummy data to simulate stock items
        #stock_table.setRowCount(1)
        #stock_table.setItem(0, 0, QTableWidgetItem("Item 1"))
        #stock_table.setItem(0, 1, QTableWidgetItem("31651"))
        #stock_table.setItem(0, 2, QTableWidgetItem("100"))
        #stock_table.setItem(0, 3, QTableWidgetItem("50"))
        #stock_table.setItem(0, 4, QTableWidgetItem("20"))
        #stock_table.setItem(0, 5, QTableWidgetItem("10.0"))

        # Add table to layout
        stock_layout.addWidget(self.stock_table, 2, 1)

        # Set central widget
        
        self.setLayout(stock_layout)

        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)
        modify_button.clicked.connect(self.modify_item)
        back_button.clicked.connect(parent.basculer_before)
        
        
    def load_stock_data(self):
        """Charger les données des produits et du stock depuis la base de données."""
        #rows = self.db_manager.get_all_stocks()

        query = """
            SELECT p.nom_produit, p.code_produit, s.qte_max, s.qte_actuelle, s.qte_min_restock, p.prix
            FROM Stocks s
            JOIN Produits p ON s.id_produit = p.id_produit
        """
        
        rows = self.conn.execute_query(query)

        # Ajouter les données dans le tableau
        self.stock_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, data in enumerate(row_data):
                self.stock_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))


    def add_item(self):
        dialog = AddModifyDialog(self, mode="Ajouter")
        dialog.exec_()

        
    def add_new_product(self, code_produit, qte_max, qte_actuelle, restock):
        """Insérer un nouveau produit dans la table Stocks uniquement, sans modifier Produits."""
        try:
            # Vérifier si le produit existe déjà dans la table Produits
            query = "SELECT id_produit FROM Produits WHERE code_produit = ?"
            result = self.conn.execute_query(query, (code_produit,))

            if not result:
                print(f"Le produit avec le code {code_produit} n'existe pas dans la table Produits.")
                return

            # Obtenir l'id du produit existant
            id_produit = result[0]["id_produit"]

            # Insérer les données dans la table Stocks
            self.conn.execute_update("""
                INSERT INTO Stocks (id_produit, qte_actuelle, qte_max, qte_min_restock)
                VALUES (?, ?, ?, ?)
            """, (id_produit, qte_actuelle, qte_max, restock))

            # Recharger les données dans le tableau
            self.load_stock_data()
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du produit dans la table Stocks: {e}")


    def remove_item(self):
        """Activer le mode sélection pour supprimer un produit."""
        # Activer la sélection dans le tableau
        self.stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stock_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Connecter l'événement de clic à la méthode `confirm_deletion`
        self.stock_table.itemClicked.connect(self.confirm_deletion)

    def confirm_deletion(self, item):
        """Demander confirmation avant de supprimer un élément."""
        # Obtenir la ligne de l'élément sélectionné
        row = item.row()

        # Récupérer les informations du produit dans la ligne sélectionnée
        nom_produit = self.stock_table.item(row, 0).text()
        code_produit = self.stock_table.item(row, 1).text()

        # Boîte de dialogue de confirmation
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Confirmer la suppression")
        confirmation_dialog.setText(f"Voulez-vous vraiment supprimer le produit '{nom_produit}' (Code: {code_produit}) ?")
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setIcon(QMessageBox.Warning)

        # Si l'utilisateur confirme la suppression
        if confirmation_dialog.exec_() == QMessageBox.Yes:
            self.delete_product(code_produit)
        else:
            # Annuler la sélection si l'utilisateur ne veut pas supprimer
            self.stock_table.clearSelection()

        # Désactiver la connexion à l'événement après la suppression ou l'annulation
        self.stock_table.itemClicked.disconnect()

    def delete_product(self, code_produit):
        """Supprimer uniquement l'entrée dans la table Stocks, sans toucher à Produits."""
        try:
            # Vérifier si le produit existe dans la table Stocks
            query = "SELECT id_produit FROM Stocks WHERE id_produit = (SELECT id_produit FROM Produits WHERE code_produit = ?)"
            result = self.conn.execute_query(query, (code_produit,))

            if not result:
                print(f"Le produit avec le code {code_produit} n'existe pas dans la table Stocks.")
                return

            # Supprimer le produit de la table Stocks
            self.conn.execute_update("DELETE FROM Stocks WHERE id_produit = (SELECT id_produit FROM Produits WHERE code_produit = ?)", (code_produit,))

            # Recharger les données dans le tableau
            self.load_stock_data()

            print(f"Le produit avec le code {code_produit} a été supprimé de la table Stocks.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression du produit : {e}")


    def modify_item(self):
        """Activer le mode sélection pour modifier un produit."""
        # Activer la sélection dans le tableau
        self.stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stock_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Connecter l'événement de clic à la méthode `open_modify_dialog`
        self.stock_table.itemClicked.connect(self.open_modify_dialog)

    def open_modify_dialog(self, item):
        row = item.row()

        # Récupérer les informations du produit dans la ligne sélectionnée
        product_data = {
            'nom': self.stock_table.item(row, 0).text(),
            'code_produit': self.stock_table.item(row, 1).text(),
            'qte_max': int(self.stock_table.item(row, 2).text()),
            'qte_actuelle': int(self.stock_table.item(row, 3).text()),
            'restock': int(self.stock_table.item(row, 4).text()),
            'prix': float(self.stock_table.item(row, 5).text())
        }

        # Ouvrir le dialogue en mode modification
        dialog = AddModifyDialog(self, mode="Modifier", product_data=product_data)
        dialog.exec_()
        
    def update_product(self, code_produit, max_qte, quantite, restock, prix):
        """Mettre à jour uniquement les informations de stock dans la table Stocks."""
        try:
            # Vérifier si le produit existe dans la table Produits
            query = "SELECT id_produit FROM Produits WHERE code_produit = ?"
            result = self.conn.execute_query(query, (code_produit,))

            if not result:
                print(f"Le produit avec le code {code_produit} n'existe pas.")
                return

            # Obtenir l'id du produit
            id_produit = result[0]["id_produit"]

            # Mettre à jour la table Stocks
            self.conn.execute_update("""
                UPDATE Stocks
                SET qte_actuelle = ?, qte_max = ?, qte_min_restock = ?
                WHERE id_produit = ?
            """, (quantite, max_qte, restock, id_produit))

            # Recharger les données dans le tableau
            self.load_stock_data()

            print(f"Les informations de stock du produit avec le code {code_produit} ont été mises à jour.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour des informations de stock : {e}")



        

