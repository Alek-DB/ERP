# fournisseur.py

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, Signal
from ERP_vue_dossier.commande import CreateOrderDialog

class QFournisseur(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__()

        self.parent = parent
        self.db_manager = db_manager

        
        layout = QGridLayout()

        
        add_button = QPushButton("Ajouter")
        modify_button = QPushButton("Modifier")
        create_order_button = QPushButton("Créer Commande")
        show_orders_button = QPushButton("Afficher Commandes")
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(modify_button)
        button_layout.addWidget(create_order_button)
        button_layout.addWidget(show_orders_button)

        layout.addLayout(button_layout, 0, 0)

        # Title
        title_label = QLabel("Gestion des Fournisseurs")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_suppliers)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout, 1, 1)

        # Suppliers table
        self.supplier_table = QTableWidget()
        self.supplier_table.setColumnCount(5)  # Ajustez le nombre de colonnes selon vos besoins
        self.supplier_table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Adresse", "Téléphone", "Email"]
        )
        layout.addWidget(self.supplier_table, 2, 1)

        
        self.setLayout(layout)

        
        self.load_data()

        
        add_button.clicked.connect(self.add_supplier)
        modify_button.clicked.connect(self.modify_supplier)
        create_order_button.clicked.connect(self.create_order)
        show_orders_button.clicked.connect(self.show_orders)
        back_button.clicked.connect(parent.basculer_vers_splash)

    def load_data(self):
        try:
            query = "SELECT * FROM Fournisseurs"
            results = self.db_manager.execute_query(query)
            self.supplier_table.setRowCount(0)  # Clear existing data

            for row_number, row_data in enumerate(results):
                self.supplier_table.insertRow(row_number)
                self.supplier_table.setItem(row_number, 0, QTableWidgetItem(str(row_data['id_fournisseur'])))
                self.supplier_table.setItem(row_number, 1, QTableWidgetItem(row_data['nom']))
                self.supplier_table.setItem(row_number, 2, QTableWidgetItem(row_data['adresse'] or ''))
                self.supplier_table.setItem(row_number, 3, QTableWidgetItem(row_data['telephone'] or ''))
                self.supplier_table.setItem(row_number, 4, QTableWidgetItem(row_data['email'] or ''))
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des données : {e}")


    def add_supplier(self):
        dialog = self.AddModifySupplierDialog(self.db_manager, mode="Ajouter")
        dialog.supplier_added.connect(self.insert_supplier_into_db)
        dialog.exec_()

    def insert_supplier_into_db(self, data):
        # Validation des données
        required_fields = ['Nom']
        for field in required_fields:
            if not data[field]:
                QMessageBox.warning(self, "Attention", f"Le champ {field} est obligatoire.")
                return

        # Insérer le fournisseur dans la base de données
        try:
            query = """
            INSERT INTO Fournisseurs (nom, adresse, telephone, email)
            VALUES (?, ?, ?, ?)
            """
            parameters = (
                data['Nom'],
                data['Adresse'] or '',
                data['Téléphone'] or '',
                data['Email'] or ''
            )

            self.db_manager.execute_update(query, parameters)
            self.load_data()
            QMessageBox.information(self, "Succès", "Fournisseur ajouté avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de l'ajout : {e}")

    def modify_supplier(self):
        selected_items = self.supplier_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un fournisseur à modifier.")
            return

        row = selected_items[0].row()
        supplier_id = self.supplier_table.item(row, 0).text()

        # Récupérer les données actuelles du fournisseur
        try:
            query = "SELECT * FROM Fournisseurs WHERE id_fournisseur = ?"
            parameters = (supplier_id,)
            result = self.db_manager.execute_query(query, parameters)
            if result:
                supplier_data = result[0]
            else:
                QMessageBox.warning(self, "Erreur", "Fournisseur non trouvé.")
                return
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite : {e}")
            return


        # Ouvrir le dialogue avec les données existantes
        dialog = self.AddModifySupplierDialog(self.db_manager, mode="Modifier", supplier_data=supplier_data)
        dialog.supplier_added.connect(lambda data: self.update_supplier_in_db(supplier_id, data))
        dialog.exec_()

    def update_supplier_in_db(self, supplier_id, data):
        # Validation des données
        required_fields = ['Nom']
        for field in required_fields:
            if not data[field]:
                QMessageBox.warning(self, "Attention", f"Le champ {field} est obligatoire.")
                return

        # Mettre à jour le fournisseur dans la base de données
        try:
            query = """
            UPDATE Fournisseurs SET nom = ?, adresse = ?, telephone = ?, email = ?
            WHERE id_fournisseur = ?
            """
            parameters = (
                data['Nom'],
                data.get('Adresse', ''),
                data.get('Téléphone', ''),
                data.get('Email', ''),
                supplier_id
            )
            self.db_manager.execute_update(query, parameters)
            self.load_data()
            QMessageBox.information(self, "Succès", "Fournisseur modifié avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la modification : {e}")

    def create_order(self):
        selected_items = self.supplier_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un fournisseur pour créer une commande.")
            return

        row = selected_items[0].row()
        supplier_id = self.supplier_table.item(row, 0).text()

        dialog = CreateOrderDialog(self.db_manager, supplier_id)
        dialog.order_created.connect(self.insert_order_into_db)
        dialog.exec_()

    def insert_order_into_db(self, data):
        # Validation des données
        required_fields = ['Produit', 'Quantité', 'Prix']
        for field in required_fields:
            if not data[field]:
                QMessageBox.warning(self, "Attention", f"Le champ {field} est obligatoire.")
                return

        try:
            # Commencer une transaction
            self.db_manager.connection.execute('BEGIN')

            # Insérer la commande dans la table Commandes
            query_commande = """
            INSERT INTO Commandes (id_fournisseur, date_commande, statut, total)
            VALUES (?, date('now'), ?, ?)
            """
            parameters_commande = (
                data['id_fournisseur'],
                'En cours',
                float(data['Prix']) * int(data['Quantité'])
            )
            self.db_manager.execute_update(query_commande, parameters_commande)

            # Récupérer l'id_commande de la commande insérée
            id_commande = self.db_manager.cursor.lastrowid

            # Récupérer l'id_produit en fonction du nom du produit
            query_produit = "SELECT id_produit FROM Produits WHERE nom_produit = ?"
            result_produit = self.db_manager.execute_query(query_produit, (data['Produit'],))
            if result_produit:
                id_produit = result_produit[0]['id_produit']
            else:
                QMessageBox.warning(self, "Erreur", "Produit non trouvé.")
                self.db_manager.connection.rollback()
                return

            # Insérer les détails du produit dans Commandes_Produits
            query_details = """
            INSERT INTO Commandes_Produits (id_commande, id_produit, quantite, prix_unitaire, total_ligne)
            VALUES (?, ?, ?, ?, ?)
            """
            parameters_details = (
                id_commande,
                id_produit,
                int(data['Quantité']),
                float(data['Prix']),
                float(data['Prix']) * int(data['Quantité'])
            )
            self.db_manager.execute_update(query_details, parameters_details)

            # Valider la transaction
            self.db_manager.connection.commit()

            QMessageBox.information(self, "Succès", "Commande créée avec succès.")

        except Exception as e:
            # Annuler la transaction en cas d'erreur
            self.db_manager.connection.rollback()
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la création de la commande : {e}")


    def show_orders(self):
        # Afficher les commandes des fournisseurs
        self.show_orders_dialog = self.AfficherCommandesFournisseur(self.db_manager)
        self.show_orders_dialog.show()

    def search_suppliers(self):
        search_text = self.search_input.text().lower()
        for row in range(self.supplier_table.rowCount()):
            item = self.supplier_table.item(row, 1)  # Nom du fournisseur
            if search_text in item.text().lower():
                self.supplier_table.setRowHidden(row, False)
            else:
                self.supplier_table.setRowHidden(row, True)

    # Classes internes pour AddModifySupplierDialog et AfficherCommandesFournisseur
    class AddModifySupplierDialog(QDialog):
        supplier_added = Signal(dict)

        def __init__(self, db_manager, mode="Ajouter", supplier_data=None):
            super().__init__()
            self.db_manager = db_manager
            self.setWindowTitle(f"{mode} Fournisseur")

            # Create the layout
            layout = QGridLayout()

            # Labels and input fields
            labels = ["Nom", "Adresse", "Téléphone", "Email"]
            self.inputs = {}

            for i, label in enumerate(labels):
                lbl = QLabel(label)
                input_field = QLineEdit()
                layout.addWidget(lbl, i, 0)
                layout.addWidget(input_field, i, 1)
                self.inputs[label] = input_field

            # Buttons for 'Ajouter/Modifier' and 'Annuler'
            self.add_modify_button = QPushButton(mode)
            self.cancel_button = QPushButton("Annuler")
            
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.add_modify_button)
            button_layout.addWidget(self.cancel_button)

            layout.addLayout(button_layout, len(labels), 1)

            # Set the layout
            self.setLayout(layout)

            # Connect cancel button to close the dialog
            self.cancel_button.clicked.connect(self.close)

            # Connect add/modify button to confirm_add method
            self.add_modify_button.clicked.connect(self.confirm_add)

            # Si nous sommes en mode "Modifier", pré-remplir les champs
            if supplier_data:
                self.fill_fields(supplier_data)

        def fill_fields(self, supplier_data):
            self.inputs['Nom'].setText(supplier_data['nom'] or '')
            self.inputs['Adresse'].setText(supplier_data['adresse'] or '')
            self.inputs['Téléphone'].setText(supplier_data['telephone'] or '')
            self.inputs['Email'].setText(supplier_data['email'] or '')



        def confirm_add(self):
            data = {label: input_field.text() for label, input_field in self.inputs.items()}
            self.supplier_added.emit(data)
            self.close()


    class AfficherCommandesFournisseur(QDialog):
        def __init__(self, db_manager):
            super().__init__()
            self.db_manager = db_manager
            self.setWindowTitle("Commandes des Fournisseurs")

            # Create the main layout
            layout = QVBoxLayout()

            # Title
            title_label = QLabel("Commandes des Fournisseurs")
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)

            # Orders table
            self.orders_table = QTableWidget()
            self.orders_table.setColumnCount(5)  # Ajustez le nombre de colonnes selon vos besoins
            self.orders_table.setHorizontalHeaderLabels(
                ["ID Commande", "Fournisseur", "Produit", "Quantité", "Prix Unitaire"]
            )
            layout.addWidget(self.orders_table)

            # Close button
            close_button = QPushButton("Fermer")
            close_button.clicked.connect(self.close)
            layout.addWidget(close_button)

            # Set layout
            self.setLayout(layout)

            # Load data
            self.load_data()

        def load_data(self):
            try:
                query = """
                SELECT c.id_commande, f.nom AS fournisseur, p.nom_produit, cp.quantite, cp.prix_unitaire
                FROM Commandes c
                JOIN Fournisseurs f ON c.id_fournisseur = f.id_fournisseur
                JOIN Commandes_Produits cp ON c.id_commande = cp.id_commande
                JOIN Produits p ON cp.id_produit = p.id_produit
                """
                results = self.db_manager.execute_query(query)
                self.orders_table.setRowCount(0)  # Clear existing data

                for row_number, row_data in enumerate(results):
                    self.orders_table.insertRow(row_number)
                    self.orders_table.setItem(row_number, 0, QTableWidgetItem(str(row_data['id_commande'])))
                    self.orders_table.setItem(row_number, 1, QTableWidgetItem(row_data['fournisseur']))
                    self.orders_table.setItem(row_number, 2, QTableWidgetItem(row_data['nom_produit']))
                    self.orders_table.setItem(row_number, 3, QTableWidgetItem(str(row_data['quantite'])))
                    self.orders_table.setItem(row_number, 4, QTableWidgetItem(str(row_data['prix_unitaire'])))
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des commandes : {e}")
