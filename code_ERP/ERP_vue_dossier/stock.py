import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager


class AddModifyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter")

        # Create the layout
        layout = QGridLayout()

        # Labels et champs de saisie
        labels = ["Nom", "Code Produit", "Max", "Quantité", "nb Restock", "Prix"]
        self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            input_field = QLineEdit()
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Buttons for 'Ajouter' and 'Annuler'
        self.add_button = QPushButton("Ajouter")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        self.add_button.clicked.connect(self.add_product)
        
        
    def add_product(self):
        """Valider les champs et ajouter le produit dans la base de données."""
        # Récupérer les valeurs des champs de saisie
        nom = self.inputs["Nom"].text()
        code_produit = self.inputs["Code Produit"].text()
        qte_max = self.inputs["Max"].text()
        qte_actuelle = self.inputs["Quantité"].text()
        restock = self.inputs["nb Restock"].text()
        prix = self.inputs["Prix"].text()

        # Vérifier que tous les champs sont remplis
        if not (nom and code_produit and qte_max and qte_actuelle and restock and prix):
            # Ajouter une validation simple
            print("Tous les champs doivent être remplis.")
            return

        # Vérifier que les valeurs numériques sont valides
        try:
            qte_max = int(qte_max)
            qte_actuelle = int(qte_actuelle)
            restock = int(restock)
            prix = float(prix)
        except ValueError:
            print("Erreur : Quantité, Restock et Prix doivent être des nombres valides.")
            return

        # Appeler la méthode de la classe parente pour insérer les données
        self.parent().add_new_product(nom, code_produit, qte_max, qte_actuelle, restock, prix)
        self.close()
        
        
class QStock(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        #set database
        self.conn = sqlite3.connect("erp_database.db")
        self.cursor = self.conn.cursor()

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
        
        
    def load_stock_data(self):
        """Charger les données des produits et du stock depuis la base de données."""
        query = """
            SELECT p.nom_produit, p.code_produit, s.qte_max, s.qte_actuelle, s.qte_min_restock, p.prix
            FROM Stocks s
            JOIN Produits p ON s.id_produit = p.id_produit
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Ajouter les données dans le tableau
        self.stock_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, data in enumerate(row_data):
                self.stock_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))


    def add_item(self):
        # Open the Add/Modify dialog
        dialog = AddModifyDialog(self)
        dialog.exec_()
        
    def add_new_product(self, nom, code_produit, qte_max, qte_actuelle, restock, prix):
        """Insérer un nouveau produit dans la base de données et le tableau."""
        try:
            
            print(nom, code_produit, qte_max, qte_actuelle, restock, prix)
            
            # Insérer les données dans la table Produits
            self.cursor.execute("""
                INSERT INTO Produits (nom_produit, code_produit, prix)
                VALUES (?, ?, ?)
            """, (nom, code_produit, prix))
            produit_id = self.cursor.lastrowid
            

            # Insérer les données dans la table Stocks
            self.cursor.execute("""
                INSERT INTO Stocks (id_produit, qte_actuelle, qte_max, qte_min_restock)
                VALUES (?, ?, ?, ?)
            """, (produit_id, qte_actuelle, qte_max, restock))
            self.conn.commit()

            # Recharger les données dans le tableau
            self.load_stock_data()
        except sqlite3.IntegrityError:
            print("Erreur : Le produit avec ce code existe déjà.")

    def remove_item(self):
        # Code to remove the selected item from the stock
        print("Remove item clicked")
        # Add logic to remove selected row from the table

    def modify_item(self):
        # Code to modify the selected item in the stock
        print("Modify item clicked")
        # Add logic to modify the selected row
        

