from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt, Signal
from ERP_emplacement import Emplacement



class QFinanceReport(QWidget):
    go_back = Signal()

    def __init__(self, parent, db):
        super().__init__()
        
        self.vue = parent
        

        
        # Layout principal
        layout = QGridLayout()
        
        self.db_manager = db

        # Bouton de retour
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        layout.addWidget(back_button, 0, 0)

        # Bouton Durée (on peut ajouter un signal ici pour appliquer des filtres si nécessaire)
        duration_button = QPushButton("Durée")
        layout.addWidget(duration_button, 0, 2)

        # Champs pour les données financières
        self.expense_field = QLineEdit()
        self.profit_field = QLineEdit()
        self.salary_field = QLineEdit()

        # Définit les champs en lecture seule
        self.expense_field.setReadOnly(True)
        self.profit_field.setReadOnly(True)
        self.salary_field.setReadOnly(True)

        # Etiquettes et champs
        layout.addWidget(QLabel("Dépense du stock"), 1, 0)
        layout.addWidget(self.expense_field, 1, 1)
        layout.addWidget(QLabel("$"), 1, 2)

        layout.addWidget(QLabel("Profit du stock"), 2, 0)
        layout.addWidget(self.profit_field, 2, 1)
        layout.addWidget(QLabel("$"), 2, 2)

        layout.addWidget(QLabel("Paiement employé"), 3, 0)
        layout.addWidget(self.salary_field, 3, 1)
        layout.addWidget(QLabel("$"), 3, 2)

        # Champ pour le total
        self.total_field = QLineEdit()
        self.total_field.setReadOnly(True)
        layout.addWidget(QLabel("Total"), 4, 0)
        layout.addWidget(self.total_field, 4, 1)
        layout.addWidget(QLabel("$"), 4, 2)

        # Bouton pour afficher un graphique
        layout.addWidget(QPushButton("Graphique"), 5, 1, 2, 1)

        self.setLayout(layout)

    def set_financial_data(self):
        
        self.succursale = Emplacement.succursalesId
        expenses = self.get_total_expenses()
        profits = self.get_total_profits()
        salaries = self.get_total_salaries()

        self.expense_field.setText(f"{expenses:.2f}")
        self.profit_field.setText(f"{profits:.2f}")
        self.salary_field.setText(f"{salaries:.2f}")

        # Calculer le total
        total = expenses + profits + salaries
        self.total_field.setText(f"{total:.2f}")
        
    def get_total_expenses(self):
        query = """
        SELECT SUM(total) AS total_expenses
        FROM Achats
        """
        result = self.db_manager.execute_query(query)
        return result[0]["total_expenses"] if result[0]["total_expenses"] is not None else 0

    def get_total_profits(self):
        query = """
        SELECT SUM(total) AS total_profits
        FROM Commandes
        WHERE statut = 'Accepter'
        """
        result = self.db_manager.execute_query(query)
        return result[0]["total_profits"] if result[0]["total_profits"] is not None else 0

    def get_total_salaries(self):
        query = """
        SELECT SUM(e.salaire) AS total_salaries
                FROM Employes e
                INNER JOIN Employes_Succursales es ON e.id_employe = es.id_employe
                WHERE es.id_succursale = ?
        """
        result = self.db_manager.execute_query(query,(self.succursale,))
        return result[0]["total_salaries"] if result[0]["total_salaries"] is not None else 0
