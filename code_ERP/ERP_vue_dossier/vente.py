from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox,QInputDialog, 
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout
)
from PySide6.QtCore import Qt

class PaymentDialog(QDialog):
    def __init__(self, total_amount, parent=None):
        super().__init__(parent)
        self.total_amount = total_amount
        self.setWindowTitle("Choisir Mode de Paiement")
        
        self.cash_button = QPushButton("Espèces")
        self.card_button = QPushButton("Carte")

        self.cash_button.clicked.connect(self.process_cash_payment)
        self.card_button.clicked.connect(self.process_card_payment)
        
        layout = QVBoxLayout()
        layout.addWidget(self.cash_button)
        layout.addWidget(self.card_button)
        
        self.setLayout(layout)
    
    def process_cash_payment(self):
        # Fenêtre pour saisir le montant d'argent donné par le client
        amount_given, ok = QInputDialog.getDouble(self, "Paiement en Espèces", 
                                                  "Montant donné par le client (en $) :", 
                                                  0, 0, 10000, 2)
        if ok:
            change = amount_given - self.total_amount
            if change < 0:
                QMessageBox.warning(self, "Erreur", "L'argent donné est insuffisant!")
            else:
                QMessageBox.information(self, "Paiement en Espèces", 
                                        f"Total: ${self.total_amount}\n"
                                        f"Argent donné: ${amount_given}\n"
                                        f"Monnaie à rendre: ${change}")
                self.accept()  # Fermeture du dialogue après le paiement

    def process_card_payment(self):
        # Fenêtre pour payer par carte
        QMessageBox.information(self, "Paiement par Carte", 
                                f"Le paiement de ${self.total_amount} a été effectué par carte.")
        self.accept()  # Fermeture du dialogue après le paiement

class Vente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vente")

        self.layout = QVBoxLayout()

        # Section informations client
        self.client_info_layout = QFormLayout()
        self.client_name_input = QLineEdit(self)
        self.client_lastname_input = QLineEdit(self)
        self.client_phone_input = QLineEdit(self)
        
        self.client_info_layout.addRow("Nom:", self.client_name_input)
        self.client_info_layout.addRow("Prénom:", self.client_lastname_input)
        self.client_info_layout.addRow("Numéro de téléphone:", self.client_phone_input)
        
        self.layout.addLayout(self.client_info_layout)

        # Section liste des produits à acheter
        self.products_table = QTableWidget(self)
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(["Produit", "Quantité", "Prix Unitaire"])
        
        # Exemple de produits pour le test
        self.add_product("Produit 1", 2, 10.0)
        self.add_product("Produit 2", 1, 15.0)

        self.layout.addWidget(self.products_table)

        # Total
        self.total_label = QLabel("Total: $0.00")
        self.layout.addWidget(self.total_label)

        # Bouton pour payer
        self.pay_button = QPushButton("Payer")
        self.pay_button.clicked.connect(self.show_payment_dialog)
        self.layout.addWidget(self.pay_button)

        self.setLayout(self.layout)

    def add_product(self, name, quantity, unit_price):
        row_position = self.products_table.rowCount()
        self.products_table.insertRow(row_position)

        self.products_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.products_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
        self.products_table.setItem(row_position, 2, QTableWidgetItem(f"${unit_price:.2f}"))
        
        self.update_total()

    def update_total(self):
        total = 0
        for row in range(self.products_table.rowCount()):
            quantity = int(self.products_table.item(row, 1).text())
            price = float(self.products_table.item(row, 2).text().strip('$'))
            total += quantity * price

        self.total_label.setText(f"Total: ${total:.2f}")
        self.total_amount = total

    def show_payment_dialog(self):
        # Ouvre la fenêtre de paiement
        payment_dialog = PaymentDialog(self.total_amount, self)
        payment_dialog.exec()

        # Après le paiement, réinitialiser les champs
        self.client_name_input.clear()
        self.client_lastname_input.clear()
        self.client_phone_input.clear()
        self.products_table.setRowCount(0)
        self.total_label.setText("Total: $0.00")
