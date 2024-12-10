import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager


class AddModifyDialog(QDialog):
    def __init__(self, parent=None, mode="Ajouter", command_data=None):
        """
        Initialise le dialogue pour ajouter ou modifier une commande.

        :param parent: La fenêtre parente
        :param mode: "Ajouter" ou "Modifier" pour déterminer le comportement du dialogue
        :param command_data: Les données de la commande à modifier (None si on ajoute une commande)
        """
        super().__init__(parent)
        self.mode = mode
        self.command_data = command_data
        self.setWindowTitle(self.mode)

        # Create the layout
        layout = QGridLayout()

        # Labels et champs de saisie
        self.inputs = {}

        lbl = QLabel("Statut")
        input_field = QComboBox()
        input_field.addItems(["En cours", "Accepter", "Refuser"])  # Options du dropdown
        layout.addWidget(lbl, 0, 0)
        layout.addWidget(input_field, 0, 1)
        self.inputs["statut"] = input_field

        # Buttons for 'Modifier' and 'Annuler'
        self.modify_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, 1, 1)

        # Set the layout
        self.setLayout(layout)

        # Connect buttons
        self.cancel_button.clicked.connect(self.close)
        self.modify_button.clicked.connect(self.modify_command)

    def modify_command(self):
        new_status = self.inputs["statut"].currentText()

        # Vérifier que les données sont valides
        if not new_status:
            QMessageBox.warning(self, "Erreur", "Le statut doit être renseigné.")
            return

        # Si "Refuser" est sélectionné, supprimer la commande
        if new_status == "Refuser":
            reply = QMessageBox.question(
                self, 
                "Confirmation de suppression", 
                "Êtes-vous sûr de vouloir supprimer cette commande ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if self.command_data:
                    command_id = self.command_data["id_commande"]
                    self.parent().delete_command(command_id)
                    QMessageBox.information(self, "Succès", "La commande a été supprimée.")
                self.close()
                return

        # Sinon, mettre à jour le statut dans la base de données
        if self.command_data:
            command_id = self.command_data["id_commande"]
            self.parent().update_command_status(command_id, new_status)

        self.close()




class QCommandeFournisseur(QWidget):
    def __init__(self, parent, db):
        super().__init__()

        self.db_manager = db
        
        self.vue = parent

        # Layout principal
        main_layout = QGridLayout()
        
        modify_button = QPushButton("Modifier")
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)

        
        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(modify_button)

        main_layout.addLayout(button_layout, 0, 0)
        
        # Titre
        title_label = QLabel("Liste des commandes")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label, 0, 1)
        
        # Tableau des commandes
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID Commande", "Fournisseur", "Commande", "Prix payé", "Date Commande", "Date de Livraison", "Adresse de Livraison", "Statut", "Notes"])
        
       
        # Ajouter des exemples de données
        self.load_supplier_payments()
        
        main_layout.addWidget(self.table, 1 , 1)
        
        # Appliquer le layout principal
        self.setLayout(main_layout)
        
        modify_button.clicked.connect(self.modify_item)

    
    def load_supplier_payments(self):
    # Requête SQL pour récupérer les achats des fournisseurs avec le prix total
        query = """
        SELECT 
            Commandes.id_commande,
            Fournisseurs.nom AS fournisseur,
            Produits.nom_produit AS produit,
            Commandes.date_commande,
            Commandes.statut,
            Commandes.total AS total_commande,
            Commandes.date_livraison,
            Commandes.adresse_livraison,
            Commandes.notes
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
                # print("Aucun paiement trouvé pour les fournisseurs.")
                return

            # Remplissage du tableau
            self.total = 0  # Réinitialiser le total

            filtered_results = [row for row in results if row["statut"] == 'En cours']  # Filtrer les résultats

            # Définir le nombre de lignes dans le tableau
            self.table.setRowCount(len(filtered_results))  

            for row, row_data in enumerate(filtered_results):
                    # Ajout des données dans le tableau
                    self.table.setItem(row, 0, QTableWidgetItem(str(row_data["id_commande"])))
                    self.table.setItem(row, 1, QTableWidgetItem(row_data["fournisseur"]))
                    self.table.setItem(row, 2, QTableWidgetItem(row_data["produit"]))
                    self.table.setItem(row, 3, QTableWidgetItem(str(row_data["total_commande"])))
                    self.table.setItem(row, 4, QTableWidgetItem(row_data["date_commande"]))
                    self.table.setItem(row, 5, QTableWidgetItem(str(row_data['date_livraison'])))
                    self.table.setItem(row, 6, QTableWidgetItem(str(row_data["adresse_livraison"])))
                    self.table.setItem(row, 7, QTableWidgetItem(row_data['statut']))
                    self.table.setItem(row, 8, QTableWidgetItem(str(row_data['notes'])))


        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de la récupération des paiements : {e}")
            
    def modify_item(self):
        """Ouvrir un dialogue de modification pour la ligne sélectionnée."""
        # Vérifiez si une ligne est sélectionnée
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une commande à modifier.")
            return

        # Récupérer la ligne sélectionnée
        row = self.table.currentRow()

        # Extraire les données de la ligne pour les passer au dialogue
        command_data = {
            "id_commande": int(self.table.item(row, 0).text()),  # ID Commande
            "statut": self.table.item(row, 7).text(),  # Colonne du statut
        }

        # Ouvrir le dialogue
        self.open_modify_dialog(command_data)


    def open_modify_dialog(self, command_data):
        """Ouvre le dialogue de modification pour les données de commande spécifiées."""
        # Créez une instance du dialogue AddModifyDialog
        dialog = AddModifyDialog(self, mode="Modifier", command_data=command_data)
        dialog.exec_()

        
    def update_command_status(self, command_id, new_status):
        """
        Met à jour le statut d'une commande dans la base de données.

        :param command_id: ID de la commande à modifier
        :param new_status: Nouveau statut
        """
        try:
            query = """
            UPDATE Commandes
            SET statut = ?
            WHERE id_commande = ?
            """
            self.db_manager.execute_query(query, (new_status, command_id))
            QMessageBox.information(self, "Succès", "Le statut de la commande a été mis à jour.")
            self.load_supplier_payments()  # Recharger les données
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de mettre à jour la commande : {e}")
            
    def delete_command(self, command_id):
        """
        Supprime une commande de la base de données.

        :param command_id: ID de la commande à supprimer
        """
        
        try:
            query = """
            DELETE FROM Commandes_Produits
            WHERE id_commande = ?
            """
            self.db_manager.execute_query(query, (command_id,))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de supprimer la commande_produits : {e}")
        
        try:
            query = """
            DELETE FROM Commandes
            WHERE id_commande = ?
            """
            self.db_manager.execute_query(query, (command_id,))
            QMessageBox.information(self, "Succès", "La commande a été supprimée.")
            self.load_supplier_payments()  # Recharger les données du tableau
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de supprimer la commande : {e}")


           

