from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Signal


class CreateOrderDialog(QDialog):
    order_created = Signal(dict)

    def __init__(self, db_manager, supplier_id):
        super().__init__()
        self.db_manager = db_manager
        self.supplier_id = supplier_id
        self.setWindowTitle("Créer Commande")

        
        layout = QGridLayout()

       
        labels = ["Produit", "Quantité", "Prix"]
        self.inputs = {}

        # Récupérer les produits depuis la base de données
        produits = self.get_produits()

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "Produit":
                input_field = QComboBox()
                input_field.addItems(produits)
            else:
                input_field = QLineEdit()
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Buttons for 'Créer Commande' and 'Annuler'
        self.create_order_button = QPushButton("Créer Commande")
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_order_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        
        self.cancel_button.clicked.connect(self.close)

        
        self.create_order_button.clicked.connect(self.confirm_create_order)

    def get_produits(self):
        query = "SELECT nom_produit FROM Produits"
        results = self.db_manager.execute_query(query)
        return [row['nom_produit'] for row in results]

    def confirm_create_order(self):
        data = {}
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                data[label] = input_field.currentText()
            else:
                data[label] = input_field.text()
        data['id_fournisseur'] = self.supplier_id
        self.order_created.emit(data)
        self.close()
