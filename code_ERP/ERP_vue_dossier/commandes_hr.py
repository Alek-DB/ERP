from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QLabel, QWidget, QTableWidget, QTableWidgetItem
)
#from ERP_vue_dossier.hr import qHRWindow

class CommandesHRWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        # Main layout for Orders interface
        main_layout = QVBoxLayout()

        # Search Box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Rechercher commande...")
        self.search_box.textChanged.connect(self.search_command)

        search_button = QPushButton("Rechercher", self)
        search_button.clicked.connect(self.search_command)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)

        # Labels for additional fields
        self.command_code_label = QLabel("Code Commande:")
        self.invoice_label = QLabel("Facture Client/Commande:")

        # Table to display order information
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)  # Adjust based on required columns
        self.order_table.setHorizontalHeaderLabels([
            "Code Commande", "Facture Client", "Date de Commande"
        ])

        # Back button to return to the previous window
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.vue.basculer_vers_hr)

        # Add widgets to the main layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.command_code_label)
        main_layout.addWidget(self.invoice_label)
        main_layout.addWidget(self.order_table)
        main_layout.addWidget(back_button)  # Adding the back button at the end

        self.setLayout(main_layout)

    def search_command(self):
        search_text = self.search_box.text().strip()
        filtered_orders = self.filter_orders(search_text)
        self.update_order_display(filtered_orders)

    #def filter_orders(self, search_text):
     #   order_dao = OrderDAO()  # Assuming you have an OrderDAO class
      #  return order_dao.get_orders_by_code_or_invoice(search_text)

    def update_order_display(self, orders):
        self.order_table.setRowCount(0)  # Clear previous results

        for order in orders:
            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)
            self.order_table.setItem(row_position, 0, QTableWidgetItem(order['id_commande']))
            self.order_table.setItem(row_position, 1, QTableWidgetItem(order['facture_client']))
            self.order_table.setItem(row_position, 2, QTableWidgetItem(order['date_commande']))

    