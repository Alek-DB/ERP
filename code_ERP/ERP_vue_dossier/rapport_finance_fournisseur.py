from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, Signal

class QFinanceFournisseurReport(QWidget):
    go_back = Signal()  # Signal pour retourner à la page précédente

    def __init__(self, parent, db):
        super().__init__()
        
        # Initialisation de la base de données
        self.db_manager = db
        
        self.vue = parent
        
        self.total = 0

        # Configuration de l'interface
        layout = QVBoxLayout()

        # Bouton de retour
        back_button = QPushButton("<-")
        back_button.setStyleSheet("background-color: #f0a500; font-weight: bold;")
        back_button.clicked.connect(self.go_back.emit)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Titre
        title = QLabel("Liste des commandes fournisseur payées")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Tableau pour les commandes et leurs prix
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Commande", "Prix payé"])
        
        
        # Étiquette pour le total
        self.total_label = QLabel("Total : ")
        self.total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.total_label)
        
        # Charger les données
        self.load_supplier_payments()
        
        layout.addWidget(self.table)

        # Ajouter le layout principal
        self.setLayout(layout)

        
        

    def load_supplier_payments(self):
    # Requête SQL pour récupérer les achats des fournisseurs avec le prix total
        query = """
            SELECT Produits.nom_produit, Fournisseurs.nom, Achats_Produits.total_ligne
            FROM Achats_Produits
            JOIN Produits ON Achats_Produits.id_produit = Produits.id_produit
            JOIN Achats ON Achats_Produits.id_achat = Achats.id_achat
            JOIN Fournisseurs ON Achats.id_fournisseur = Fournisseurs.id_fournisseur
        """
        
        # Exécuter la requête
        results = self.db_manager.execute_query(query)

        # Remplissage du tableau
        self.table.setRowCount(len(results))
        self.total = 0  # Réinitialiser le total
        for row, row_data in enumerate(results):
            # Ajout des données dans le tableau
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data["nom_produit"])))
            self.table.setItem(row, 1, QTableWidgetItem(f"{row_data['nom']:.2f} €"))
            
            # Calcul du total
            self.total += row_data["total_ligne"]

        # Mise à jour du total dans le label
        self.total_label.setText(f"Total : {self.total:.2f} €")
