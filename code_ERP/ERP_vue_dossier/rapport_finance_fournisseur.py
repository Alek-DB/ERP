import sqlite3
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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Fournisseur", "Commande", "Prix payé", "Statut"])
        
        
        # Étiquette pour le total
        self.total_label = QLabel("Total : ")
        self.total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.total_label)
        
        # Charger les données
        self.load_supplier_payments()
        
        layout.addWidget(self.table)

        # Ajouter le layout principal
        self.setLayout(layout)
        
        self.print_all_commandes()

        
        
    def print_all_commandes(self):
    # Requête pour sélectionner toutes les colonnes et lignes de la table Commandes
        query = "SELECT * FROM Commandes"
        # Exécuter la requête
        results = self.db_manager.execute_query(query)
        
        # Vérifier s'il y a des résultats
        if not results:
            print("La table Commandes est vide.")
            return

        # Parcourir et afficher chaque ligne
        # print("Contenu de la table Commandes :")
        # for row in results:
        #     print(dict(row))  # Convertit la ligne en dictionnaire pour un affichage lisible

        

        

    def load_supplier_payments(self):
    # Requête SQL pour récupérer les achats des fournisseurs avec le prix total
        query = """
        SELECT 
            Fournisseurs.nom AS fournisseur,
            Produits.nom_produit AS produit,
            Commandes.total AS total_commande,
            Commandes.statut
            FROM Commandes
            JOIN Commandes_Produits ON Commandes.id_commande = Commandes_Produits.id_commande
            JOIN Produits ON Commandes_Produits.id_produit = Produits.id_produit
            JOIN Fournisseurs ON Commandes.id_fournisseur = Fournisseurs.id_fournisseur
        """
        
        try:
            # Exécuter la requête et récupérer les résultats
            results = self.db_manager.execute_query(query)

            # Si aucun résultat, afficher un message
            if not results:
                print("Aucun paiement trouvé pour les fournisseurs.")
                return

            # Remplissage du tableau
            self.total = 0  # Réinitialiser le total
            
            filtered_results = [row for row in results if row["statut"] != 'En cours']  # Filtrer les résultats

            # Définir le nombre de lignes dans le tableau
            self.table.setRowCount(len(filtered_results))  

            for row, row_data in enumerate(filtered_results):
                # Ajout des données dans le tableau
                self.table.setItem(row, 0, QTableWidgetItem(row_data["fournisseur"]))
                self.table.setItem(row, 1, QTableWidgetItem(row_data["produit"]))
                self.table.setItem(row, 2, QTableWidgetItem(str(row_data["total_commande"])))
                self.table.setItem(row, 3, QTableWidgetItem(row_data['statut']))

                # Calcul du total des paiements
                self.total += row_data["total_commande"]

            # Mise à jour du total dans le label
            self.total_label.setText(f"Total : {self.total:.2f} $")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de la récupération des paiements : {e}")
