from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QDialog,
    QLabel, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from ERP_data_base import DatabaseManager


class ModifyOrderDialog(QDialog):
    order_modified = Signal(dict)

    def __init__(self, db_manager, order_data):
        super().__init__()
        
        self.db_manager = db_manager
        self.order_data = order_data
        self.setWindowTitle("Modifier Commande")

        layout = QGridLayout()
        labels = ["Produit", "Quantité", "Prix"]
        self.inputs = {}

        produits = self.get_produits()

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "Produit":
                input_field = QComboBox()
                input_field.addItems(produits)
                input_field.setCurrentText(self.order_data['produit']) 
            else:
                input_field = QLineEdit(str(self.order_data[label.lower()]))
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        self.save_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)
        self.setLayout(layout)

        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.confirm_modify_order)

    def get_produits(self):
        query = "SELECT nom_produit FROM Produits"
        results = self.db_manager.execute_query(query)
        return [row['nom_produit'] for row in results]

    def confirm_modify_order(self):
        data = {}
        for label, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                data[label] = input_field.currentText()
            else:
                data[label] = input_field.text()

        # Validate inputs before proceeding
        if not self.validate_inputs(data):
            return  # Exit the method if validation fails

        data['id_commande'] = self.order_data['id_commande']

        # Proceed to update the order in the database
        self.update_order_in_db(data)
        self.order_modified.emit(data)
        self.close()


    def update_order_in_db(self, data):
        query = """
        UPDATE Commandes
        SET produit = ?, quantite = ?, prix = ?
        WHERE id_commande = ?
        """
        self.db_manager.execute_update(query, (data['Produit'], data['Quantité'], data['Prix'], data['id_commande']))
        QMessageBox.information(self, "Succès", "Commande modifiée avec succès.")

    def validate_inputs(self, data):
        try:
            # Validate that the quantity is a valid integer
            quantity = int(data['Quantité'])
            # Validate that the price is a valid float
            price = float(data['Prix'])
            
            # Optionally, check that the values are positive numbers
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantité et prix doivent être supérieurs à zéro.")
            
            return True
        except ValueError as e:
            # Display a warning if validation fails
            QMessageBox.warning(self, "Erreur de validation", str(e) if str(e) else "La quantité ou le prix est invalide.")
            return False



class CommandesHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.vue = parent
        self.db_manager = DatabaseManager('erp_database.db')  # Make sure this line exists
        self.setWindowTitle("Gestion des Commandes")

        # Main layout
        main_layout = QVBoxLayout()

        # Search box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Rechercher commande...")
        self.search_box.textChanged.connect(self.search_order)

        search_button = QPushButton("Rechercher", self)
        search_button.clicked.connect(self.search_order)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)

      # Table to display employee information
        self.orders_table = QTableWidget()
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.orders_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.orders_table.cellClicked.connect(self.on_order_select)
        
        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(parent.basculer_before)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.orders_table)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def search_order(self):
        search_text = self.search_box.text().strip()
        orders = self.get_orders_by_id(search_text)
        self.update_order_display(orders)

    def get_orders_by_id(self, order_id):
        query = "SELECT id_commande, produit, quantite, prix FROM Commandes WHERE id_commande LIKE ?"
        return self.db_manager.execute_query(query, ('%' + order_id + '%',))

    def update_order_display(self, orders):
        self.orders_table.setRowCount(0)  

        if not orders:
            QMessageBox.warning(self, "Aucun résultat", "Aucune commande trouvée.")
            return

        for order in orders:
            row_position = self.orders_table.rowCount()
            self.orders_table.insertRow(row_position)
            self.orders_table.setItem(row_position, 0, QTableWidgetItem(str(order['id_commande'])))
            self.orders_table.setItem(row_position, 1, QTableWidgetItem(order['produit']))
            self.orders_table.setItem(row_position, 2, QTableWidgetItem(str(order['quantite'])))
            self.orders_table.setItem(row_position, 3, QTableWidgetItem(str(order['prix'])))

    def on_order_select(self, row, column):
        """Cuando se selecciona una fila, abre el diálogo para modificar la orden."""
        order_id = self.orders_table.item(row, 0).text()
        self.open_modify_dialog(order_id)

    def open_modify_dialog(self, order_id):
        """Abre el diálogo de modificación de la orden."""
        query = "SELECT id_commande, produit, quantite, prix FROM Commandes WHERE id_commande = ?"
        order_data = self.db_manager.execute_query(query, (order_id,))

        if order_data:
            order_data = order_data[0] 
            dialog = ModifyOrderDialog(self.db_manager, order_data)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Erreur", "Commande introuvable avec cet ID.")
