from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

class QFinance(QWidget):
    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__()

        # Layout principal
        layout = QGridLayout()
        
        self.vue = parent

        # Bouton de retour
        back_button = QPushButton("<-")
        back_button.clicked.connect(self.go_back.emit)  # Émet le signal pour revenir en arrière
        layout.addWidget(back_button, 0, 0)

        # Boutons principaux
        report_finance_button = QPushButton("Rapport de finance")
        report_supplier_finance_button = QPushButton("Rapport de finance fournisseur")
        supplier_order_button = QPushButton("Commande Fournisseur")

        # Style des boutons (facultatif)
        button_style = "background-color: #f0a500; padding: 20px; font-size: 14px; font-weight: bold;"
        report_finance_button.setStyleSheet(button_style)
        report_finance_button.clicked.connect(self.show_finance_report)

        report_supplier_finance_button.setStyleSheet(button_style)
        report_supplier_finance_button.clicked.connect(self.show_supplier_report)
        
        supplier_order_button.setStyleSheet(button_style)

        # Ajout des boutons au layout
        layout.addWidget(report_finance_button, 1, 1)
        layout.addWidget(report_supplier_finance_button, 1, 2)
        layout.addWidget(supplier_order_button, 1, 3)

        self.setLayout(layout)
        
    def show_finance_report(self):
        self.vue.basculer_vers_finance_report()
        
    def show_supplier_report(self):
        self.vue.basculer_vers_fournisseur_report()
    
