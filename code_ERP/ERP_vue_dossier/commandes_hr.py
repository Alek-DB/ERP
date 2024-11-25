import sqlite3
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog
)
from ERP_data_base import DatabaseManager

class CommandesHRWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Order Management")
        self.resize(800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search for an order...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_orders)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)

        # Table to display orders
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)  # Adjust the number of columns as needed
        self.orders_table.setHorizontalHeaderLabels([
            "Order ID", "Employee", "Date", "Status", "Total Amount"
        ])
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.orders_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.orders_table.cellClicked.connect(self.on_order_select)

        # Buttons for managing orders
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        modify_button = QPushButton("Modify")
        delete_button = QPushButton("Delete")

        add_button.clicked.connect(self.add_order)
        modify_button.clicked.connect(self.modify_order)
        delete_button.clicked.connect(self.delete_order)

        button_layout.addWidget(add_button)
        button_layout.addWidget(modify_button)
        button_layout.addWidget(delete_button)

        # Add widgets to the main layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Load orders on initialization
        self.load_orders()

    def load_orders(self):
        """Load all orders into the table."""
        db_manager = DatabaseManager("erp_database.db")
        try:
            query = "SELECT id_commande, employe, date, statut, montant_total FROM Commandes"
            orders = db_manager.execute_query(query)

            self.orders_table.setRowCount(0)  # Clear the table

            for order in orders:
                row_position = self.orders_table.rowCount()
                self.orders_table.insertRow(row_position)
                for col, value in enumerate(order):
                    self.orders_table.setItem(row_position, col, QTableWidgetItem(str(value)))

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def search_orders(self):
        """Search for orders based on the entered text."""
        search_text = self.search_box.text().strip()
        db_manager = DatabaseManager("erp_database.db")
        try:
            query = "SELECT id_commande, employe, date, statut, montant_total FROM Commandes WHERE employe LIKE ?"
            orders = db_manager.execute_query(query, (f"%{search_text}%",))
            self.update_table(orders)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def update_table(self, orders):
        """Update the table with filtered orders."""
        self.orders_table.setRowCount(0)  # Clear the table

        for order in orders:
            row_position = self.orders_table.rowCount()
            self.orders_table.insertRow(row_position)
            for col, value in enumerate(order):
                self.orders_table.setItem(row_position, col, QTableWidgetItem(str(value)))

    def add_order(self):
        """Open a dialog to add a new order."""
        dialog = AddModifyOrderDialog(self, mode="Add")
        if dialog.exec():
            self.load_orders()

    def modify_order(self):
        """Open a dialog to modify the selected order."""
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an order to modify.")
            return

        order_id = self.orders_table.item(selected_row, 0).text()
        db_manager = DatabaseManager("erp_database.db")
        try:
            query = "SELECT * FROM Commandes WHERE id_commande = ?"
            order = db_manager.execute_query(query, (order_id,))
            if order:
                dialog = AddModifyOrderDialog(self, mode="Modify", order_data=order[0])
                if dialog.exec():
                    self.load_orders()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def delete_order(self):
        """Delete the selected order."""
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an order to delete.")
            return

        order_id = self.orders_table.item(selected_row, 0).text()
        confirm = QMessageBox.question(
            self, "Confirmation", f"Are you sure you want to delete order {order_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            db_manager = DatabaseManager("erp_database.db")
            try:
                query = "DELETE FROM Commandes WHERE id_commande = ?"
                db_manager.execute_update(query, (order_id,))
                QMessageBox.information(self, "Success", "Order successfully deleted.")
                self.load_orders()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        
    def on_order_select(self, row, _):
        """Handles the event when a row in the orders table is selected."""
        # Retrieve the order ID from the first column
        cell = self.orders_table.item(row, 0)
        if not cell:
            QMessageBox.warning(self, "Error", "Invalid row selection. Please select a valid order.")
            return

        selected_order_id = cell.text()  # Assuming the first column contains the order ID

        # Fetch additional details for the selected order
        db_manager = DatabaseManager("erp_database.db")
        try:
            query = "SELECT * FROM Commandes WHERE id_commande = ?"
            order = db_manager.execute_query(query, (selected_order_id,))
            if order:
                # If an order is found, display details (adjust the format to your needs)
                order_details = "\n".join(f"{key}: {value}" for key, value in zip(db_manager.get_column_names("Commandes"), order[0]))
                QMessageBox.information(self, "Order Selected", f"Order ID: {selected_order_id}\nDetails:\n{order_details}")
            else:
                QMessageBox.warning(self, "Error", "No details found for the selected order.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
