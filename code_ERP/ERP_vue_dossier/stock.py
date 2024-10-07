import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog
)
from PySide6.QtCore import Qt




class AddModifyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter")

        # Create the layout
        layout = QGridLayout()

        # Labels and input fields
        labels = ["Min", "Max", "Quantité", "Nom", "nb Restock", "Prix", "futur champ*"]
        self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            input_field = QLineEdit()
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
        
        
class QStock(QWidget):
    def __init__(self, parent):
        super().__init__()

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
        stock_table = QTableWidget()
        stock_table.setColumnCount(5)
        stock_table.setHorizontalHeaderLabels(
            ["Liste (nom/code)", "max", "qte", "restock", "prix"]
        )
        
        # Dummy data to simulate stock items
        stock_table.setRowCount(3)
        stock_table.setItem(0, 0, QTableWidgetItem("Item 1"))
        stock_table.setItem(0, 1, QTableWidgetItem("100"))
        stock_table.setItem(0, 2, QTableWidgetItem("50"))
        stock_table.setItem(0, 3, QTableWidgetItem("20"))
        stock_table.setItem(0, 4, QTableWidgetItem("10.0"))
        stock_table.setItem(1, 0, QTableWidgetItem("Item 2"))
        stock_table.setItem(1, 1, QTableWidgetItem("200"))
        stock_table.setItem(1, 2, QTableWidgetItem("150"))
        stock_table.setItem(1, 3, QTableWidgetItem("50"))
        stock_table.setItem(1, 4, QTableWidgetItem("20.0"))
        stock_table.setItem(2, 0, QTableWidgetItem("Item 3"))
        stock_table.setItem(2, 1, QTableWidgetItem("50"))
        stock_table.setItem(2, 2, QTableWidgetItem("30"))
        stock_table.setItem(2, 3, QTableWidgetItem("10"))
        stock_table.setItem(2, 4, QTableWidgetItem("5.00"))

        # Add table to layout
        stock_layout.addWidget(stock_table, 2, 1)

        # Set central widget
        
        self.setLayout(stock_layout)

        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)
        modify_button.clicked.connect(self.modify_item)

    def add_item(self):
        # Open the Add/Modify dialog
        dialog = AddModifyDialog()
        dialog.exec_()

    def remove_item(self):
        # Code to remove the selected item from the stock
        print("Remove item clicked")
        # Add logic to remove selected row from the table

    def modify_item(self):
        # Code to modify the selected item in the stock
        print("Modify item clicked")
        # Add logic to modify the selected row