
import sqlite3
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from ERP_data_base import DatabaseManager


class HR_Commandes(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.vue = parent
        #set database
        self.db_manager = DatabaseManager('erp_database.db')

        # Main layout for Employee interface
        hrCommande_layout = QGridLayout()

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
        hrCommande_layout.addLayout(button_layout, 0, 0)

        # Title of the Commandes HR
        title_label = QLabel("Commandes HR")
        title_label.setAlignment(Qt.AlignCenter)
        hrCommande_layout.addWidget(title_label, 0, 1)
        
        # Search bar
        search_label = QLabel("Rechercher :")
        search_input = QLineEdit()

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        hrCommande_layout.addLayout(search_layout, 1, 1)
        
        self.commandeHR_table = QTableWidget()
        self.commandeHR_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.commandeHR_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.commandeHR_table.setSelectionMode(QTableWidget.SingleSelection)
        self.modify_item()
        self.setLayout(hrCommande_layout)
        self.load_commande()

        # Add table to layout
        hrCommande_layout.addWidget(self.succursale_table, 2, 1)
        
        
        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.modify_button.clicked.connect(self.modify_item)
        self.open_button.clicked.connect(self.open_commande)
        back_button.clicked.connect(self.vue.basculer_before)

    def load_commande(self):
            try: #toy aca
                db_manager = DatabaseManager('erp_database.db')
                # METTRE LE NOM DE VOTRE TABLE ET LES VALEURS A AFFICHER DANS LA LISTE
                query = "SELECT code_produit, nom_produit, prix, Succursale FROM Produits"
                self.commandeHR_table.setColumnCount(4) # METTRE LE MEME DE COLONNE
                rows = db_manager.execute_query(query, ())
                self.commandeHR_table.setHorizontalHeaderLabels(["Nom", "Quantité", "Prix", "Succursale"])

                self.commandeHR_table.setRowCount(len(rows))
                for row_index, row_data in enumerate(rows):
                    for col_index, data in enumerate(row_data):
                        self.commandeHR_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            except sqlite3.Error as e:
                print(f"Une erreur est survenue : {e}")

    def open_modify_dialog(self, item):
            row = item.row()

            succursale_id = self.commandeHR_table.item(row, 0).text()  # Ajustez selon votre structure

            # Étape 1: Sélectionner toutes les colonnes de la table
            # METTRE LE NOM DE VOTRE TABLE ICI
            query = "SELECT * FROM succursales WHERE id_succursale = ?"
            result = self.db_manager.execute_query(query, (succursale_id,))

            # Récupérer toutes les valeurs dans un tableau
            product_data = []
            if result:
                product_data = list(result[0])  # Convertir le tuple en liste

            # Ouvrir le dialogue en mode modification
            dialog = AddModifyDialog(self, mode="Modifier", product_data=product_data)
            dialog.exec_()