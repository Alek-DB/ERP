# client.py

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QDialog, QFormLayout, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, Signal
from ERP_data_base import DatabaseManager
import sqlite3
import ERP_regle_affaire as regle
from ERP_vue_dossier.rabais import Rabais

class QClient(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__()

        self.parent = parent
        self.db_manager = db_manager

        layout = QGridLayout()

        # Boutons sur la gauche
        add_button = QPushButton("Ajouter Client")
        modify_button = QPushButton("Modifier Client")
        info_button = QPushButton("Informations")
        create_order_button = QPushButton("Créer Commande")  # Nouveau bouton
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(modify_button)
        button_layout.addWidget(info_button)
        button_layout.addWidget(create_order_button)  # Ajouter le bouton au layout

        layout.addLayout(button_layout, 0, 0)

        # Titre
        title_label = QLabel("Gestion des Clients")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 0, 1)

        # Barre de recherche
        search_label = QLabel("Rechercher :")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_clients)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout, 1, 1)

        # Tableau des clients
        self.client_table = QTableWidget()
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.client_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.client_table.setSelectionMode(QTableWidget.SingleSelection)
        self.client_table.setColumnCount(5)  # Code, Prenom, Nom, Factures, Commandes
        self.client_table.setHorizontalHeaderLabels(
            ["Code", "Prenom", "Nom", "Factures", "Commandes"]
        )
        self.client_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.client_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.client_table, 2, 1)

        self.setLayout(layout)

        # Charger les données
        self.load_data()

        # Connecter les boutons
        add_button.clicked.connect(self.add_client)
        modify_button.clicked.connect(self.modify_client)
        info_button.clicked.connect(self.show_client_info)
        create_order_button.clicked.connect(self.create_order)  # Connecter le nouveau bouton
        back_button.clicked.connect(parent.basculer_before)

    def load_data(self):
        try:
            # Aller chercher tous les clients
            query_clients = "SELECT * FROM Clients"
            clients = self.db_manager.execute_query(query_clients)

            self.client_table.setRowCount(0)  # Vider les données existantes

            for row_number, client in enumerate(clients):
                client_id = client['id_client']

                # Aller chercher les commandes du client
                query_commandes = "SELECT * FROM Commandes WHERE id_client = ?"
                commandes = self.db_manager.execute_query(query_commandes, (client_id,))
                nb_commandes = len(commandes)

                # Calculer le total des factures
                total_factures = sum(commande['total'] or 0 for commande in commandes)

                self.client_table.insertRow(row_number)
                self.client_table.setItem(row_number, 0, QTableWidgetItem(str(client_id)))
                self.client_table.setItem(row_number, 1, QTableWidgetItem(str(client["prenom"])))
                self.client_table.setItem(row_number, 2, QTableWidgetItem(str(client["nom"])))
                self.client_table.setItem(row_number, 3, QTableWidgetItem(f"{total_factures:.2f}"))
                self.client_table.setItem(row_number, 4, QTableWidgetItem(str(nb_commandes)))

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des données : {e}")

    def add_client(self):
        dialog = self.AddModifyDialog(self.db_manager, mode="Ajouter")
        dialog.client_added.connect(self.insert_client_into_db)
        dialog.exec_()

    def insert_client_into_db(self, data):
        # Validation des données
        # required_fields = ['Nom', 'Prenom', 'Statut']
        # for field in required_fields:
        #     if not data.get(field):
        #         QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
        #         return

        # # Vérification des types de données si nécessaire

        # # Insérer le client dans la base de données
        # try:
        #     query = """
        #     INSERT INTO Clients (nom, prenom, adresse, telephone, email, date_inscription, statut, notes)
        #     VALUES (?, ?, ?, ?, ?, date('now'), ?, ?)
        #     """
        #     parameters = (
        #         data['Nom'],
        #         data['Prenom'],
        #         data.get('Adresse', ''),
        #         data.get('Telephone', ''),
        #         data.get('Email', ''),
        #         data['Statut'],
        #         data.get('Notes', '')
        #     )

        #     self.db_manager.execute_update(query, parameters)
            self.load_data()
        # except Exception as e:
        #     QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de l'ajout : {e}")

    def modify_client(self):
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un client à modifier.")
            return

        row = selected_items[0].row()
        client_id = self.client_table.item(row, 0).text()

        # Récupérer les données actuelles du client
        try:
            query = "SELECT * FROM Clients WHERE id_client = ?"
            parameters = (client_id,)
            result = self.db_manager.execute_query(query, parameters)
            if result:
                client_data = result[0]
            else:
                QMessageBox.warning(self, "Erreur", "Client non trouvé.")
                return
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite : {e}")
            return

        # Ouvrir le dialogue avec les données existantes
        dialog = self.AddModifyDialog(self.db_manager, mode="Modifier", client_data=client_data)
        dialog.client_added.connect(lambda data: self.update_client_in_db(client_id, data))
        dialog.exec_()

    def update_client_in_db(self, client_id, data):
        # Validation des données
        required_fields = ['Nom', 'Prenom', 'Statut']
        for field in required_fields:
            if not data.get(field):
                QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
                return

        # Vérification des types de données si nécessaire

        # Mettre à jour le client dans la base de données
        try:
            query = """
            UPDATE Clients SET nom = ?, prenom = ?, adresse = ?, telephone = ?, email = ?, statut = ?, notes = ?
            WHERE id_client = ?
            """
            parameters = (
                data['Nom'],
                data['Prenom'],
                data.get('Adresse', ''),
                data.get('Telephone', ''),
                data.get('Email', ''),
                data['Statut'],
                data.get('Notes', ''),
                client_id
            )
            self.db_manager.execute_update(query, parameters)
            self.load_data()
            QMessageBox.information(self, "Succès", "Client modifié avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la modification : {e}")

    def show_client_info(self):
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un client pour afficher les informations.")
            return

        row = selected_items[0].row()
        client_id = self.client_table.item(row, 0).text()

        # Ouvrir la fenêtre d'informations du client
        dialog = self.ClientInfoDialog(self.db_manager, client_id)
        dialog.exec_()

    def create_order(self):
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un client pour créer une commande.")
            return

        row = selected_items[0].row()
        client_id = int(self.client_table.item(row, 0).text())

        # Ouvrir le dialogue de création de commande pour le client sélectionné
        dialog = self.CreateOrderDialog(self.db_manager, client_id)
        dialog.order_created.connect(self.on_order_created)
        dialog.exec_()

    def on_order_created(self, data):
        # Mettre à jour les données si nécessaire
        self.load_data()

    def search_clients(self):
        search_text = self.search_input.text().lower()
        for row in range(self.client_table.rowCount()):
            code_item = self.client_table.item(row, 0)  # Code du client
            if search_text in code_item.text().lower():
                self.client_table.setRowHidden(row, False)
            else:
                self.client_table.setRowHidden(row, True)

    # Classes internes pour AddModifyDialog, ClientInfoDialog et CreateOrderDialog
    class AddModifyDialog(QDialog):
        client_added = Signal(dict)

        def __init__(self, db_manager, mode="Ajouter", client_data=None):
            super().__init__()
            self.db_manager = db_manager
            self.mode = mode
            self.client_data = client_data

            self.setWindowTitle(f"{self.mode} Client")

            # Créer la mise en page
            layout = QGridLayout()

            # Labels et champs de saisie
            labels = ["Nom", "Prenom", "Adresse", "Telephone", "Email", "Statut", "Notes"]
            self.inputs = {}

            for i, label in enumerate(labels):
                lbl = QLabel(label)
                if label == "Statut":
                    # Créer un QComboBox pour le champ Statut avec des options prédéfinies
                    input_field = QComboBox()
                    input_field.addItems(["Actif", "Inactif"])
                else:
                    input_field = QLineEdit()
                layout.addWidget(lbl, i, 0)
                layout.addWidget(input_field, i, 1)
                self.inputs[label] = input_field

            # Boutons 'Ajouter/Modifier' et 'Annuler'
            self.add_modify_button = QPushButton(mode)
            self.cancel_button = QPushButton("Annuler")
            self.cancel_button.clicked.connect(self.close)

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.add_modify_button)
            button_layout.addWidget(self.cancel_button)

            layout.addLayout(button_layout, len(labels), 1)

            # Définir la mise en page
            self.setLayout(layout)

            # Connecter le bouton ajouter/modifier à la méthode appropriée
            if self.mode == "Ajouter":
                self.add_modify_button.clicked.connect(self.enregistrer)
            else:
                self.add_modify_button.clicked.connect(self.modify_client)

            # Si nous sommes en mode "Modifier", pré-remplir les champs
            if self.mode == "Modifier" and self.client_data:
                self.fill_fields(self.client_data)

        def fill_fields(self, client_data):
            self.inputs['Nom'].setText(client_data['nom'] or '')
            self.inputs['Prenom'].setText(client_data['prenom'] or '')
            self.inputs['Adresse'].setText(client_data['adresse'] or '')
            self.inputs['Telephone'].setText(client_data['telephone'] or '')
            self.inputs['Email'].setText(client_data['email'] or '')
            statut = client_data['statut'] or 'Actif'
            index = self.inputs['Statut'].findText(statut)
            if index >= 0:
                self.inputs['Statut'].setCurrentIndex(index)
            self.inputs['Notes'].setText(client_data['notes'] or '')

        def enregistrer(self):
            data = {}
            for label, input_field in self.inputs.items():
                if isinstance(input_field, QComboBox):
                    data[label] = input_field.currentText()
                else:
                    data[label] = input_field.text()

            # Validation des champs obligatoires
            required_fields = ['Nom', 'Prenom', 'Statut']
            for field in required_fields:
                if not data.get(field):
                    QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
                    return

            # Insérer le client dans la base de données
            try:
                query = """
                INSERT INTO Clients (nom, prenom, adresse, telephone, email, date_inscription, statut, notes)
                VALUES (?, ?, ?, ?, ?, date('now'), ?, ?)
                """
                parameters = (
                    data['Nom'],
                    data['Prenom'],
                    data.get('Adresse', ''),
                    data.get('Telephone', ''),
                    data.get('Email', ''),
                    data['Statut'],
                    data.get('Notes', '')
                )

                self.db_manager.execute_update(query, parameters)
                self.client_added.emit(data)  # Émettre le signal pour mettre à jour le tableau
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de l'ajout : {e}")


        def modify_client(self):
            data = {}
            for label, input_field in self.inputs.items():
                if isinstance(input_field, QComboBox):
                    data[label] = input_field.currentText()
                else:
                    data[label] = input_field.text()

            # Validation des champs obligatoires
            required_fields = ['Nom', 'Prenom', 'Statut']
            for field in required_fields:
                if not data.get(field):
                    QMessageBox.warning(self, "Attention", f"Le champ '{field}' est obligatoire.")
                    return

            # Émettre le signal avec les données modifiées
            self.client_added.emit(data)
            self.close()


    class ClientInfoDialog(QDialog):
        def __init__(self, db_manager, client_id):
            super().__init__()
            self.db_manager = db_manager
            self.client_id = client_id
            self.setWindowTitle("Informations du Client")

            # Créer la mise en page principale
            layout = QVBoxLayout()

            # Titre
            title_label = QLabel("Détails du Client")
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)

            # Afficher les informations du client
            client_info_layout = QFormLayout()
            self.labels = {}
            info_labels = ["Nom", "Prenom", "Adresse", "Telephone", "Email", "Date d'inscription", "Statut", "Notes"]
            for label in info_labels:
                lbl = QLabel()
                client_info_layout.addRow(f"{label} :", lbl)
                self.labels[label] = lbl

            layout.addLayout(client_info_layout)

            # Tableau des commandes
            commandes_label = QLabel("Commandes")
            commandes_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(commandes_label)

            self.commandes_table = QTableWidget()
            self.commandes_table.setColumnCount(4)
            self.commandes_table.setHorizontalHeaderLabels(
                ["ID Commande", "Date", "Statut", "Total"]
            )
            layout.addWidget(self.commandes_table)

            # Bouton Fermer
            close_button = QPushButton("Fermer")
            close_button.clicked.connect(self.close)
            layout.addWidget(close_button)

            # Définir la mise en page
            self.setLayout(layout)

            # Charger les données du client
            self.load_client_info()

        def load_client_info(self):
            try:
                # Charger les informations du client
                query = "SELECT * FROM Clients WHERE id_client = ?"
                parameters = (self.client_id,)
                result = self.db_manager.execute_query(query, parameters)
                if result:
                    client_data = result[0]
                    self.labels['Nom'].setText(client_data['nom'])
                    self.labels['Prenom'].setText(client_data['prenom'])
                    self.labels['Adresse'].setText(client_data['adresse'] or '')
                    self.labels['Telephone'].setText(client_data['telephone'] or '')
                    self.labels['Email'].setText(client_data['email'] or '')
                    self.labels["Date d'inscription"].setText(client_data['date_inscription'] or '')
                    self.labels['Statut'].setText(client_data['statut'] or '')
                    self.labels['Notes'].setText(client_data['notes'] or '')
                else:
                    QMessageBox.warning(self, "Erreur", "Client non trouvé.")
                    return

                # Charger les commandes du client
                query_commandes = "SELECT * FROM Commandes WHERE id_client = ?"
                commandes = self.db_manager.execute_query(query_commandes, (self.client_id,))
                self.commandes_table.setRowCount(0)
                for row_number, commande in enumerate(commandes):
                    self.commandes_table.insertRow(row_number)
                    self.commandes_table.setItem(row_number, 0, QTableWidgetItem(str(commande['id_commande'])))
                    self.commandes_table.setItem(row_number, 1, QTableWidgetItem(commande['date_commande'] or ''))
                    self.commandes_table.setItem(row_number, 2, QTableWidgetItem(commande['statut'] or ''))
                    self.commandes_table.setItem(row_number, 3, QTableWidgetItem(f"{commande['total'] or 0:.2f}"))

                # Vous pouvez également ajouter des sections pour les factures et les paiements

            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors du chargement des informations : {e}")

    class CreateOrderDialog(QDialog):
        order_created = Signal(dict)

        def __init__(self, db_manager, client_id):
            super().__init__()
            self.db_manager = db_manager
            self.client_id = client_id
            self.setWindowTitle("Créer Commande")
            
            
            self.all_rabais = regle.verify_regles(self.db_manager, client_id)
            if self.all_rabais: 
                text = ""
                for rabais in self.all_rabais:
                    text += rabais.title + "\n"
                QMessageBox.warning(self, "Attention", text)
            

            layout = QVBoxLayout()

            # Informations du client
            client_info_layout = QFormLayout()
            self.labels = {}
            client_data = self.get_client_info()
            if client_data:
                info_labels = ["Nom", "Prenom", "Email", "Telephone"]
                for label in info_labels:
                    lbl = QLabel(str(client_data[label.lower()]))
                    client_info_layout.addRow(f"{label} :", lbl)
                    self.labels[label] = lbl
            else:
                QMessageBox.warning(self, "Erreur", "Client non trouvé.")
                self.close()
                return

            layout.addLayout(client_info_layout)

            # Sélection des produits
            product_layout = QHBoxLayout()
            product_label = QLabel("Produit :")
            self.product_combo = QComboBox()
            produits = self.get_produits()
            self.product_combo.addItems([f"{p['id_produit']} - {p['nom_produit']} - {p['prix']}" for p in produits])
            product_layout.addWidget(product_label)
            product_layout.addWidget(self.product_combo)

            # Quantité
            quantity_layout = QHBoxLayout()
            quantity_label = QLabel("Quantité :")
            self.quantity_input = QSpinBox()
            self.quantity_input.setMinimum(1)
            quantity_layout.addWidget(quantity_label)
            quantity_layout.addWidget(self.quantity_input)

            # Ajouter produit au panier
            add_product_button = QPushButton("Ajouter au Panier")
            add_product_button.clicked.connect(self.add_product_to_cart)

            # Tableau du panier
            self.cart_table = QTableWidget()
            self.cart_table.setColumnCount(4)
            self.cart_table.setHorizontalHeaderLabels(["ID Produit", "Nom", "Quantité", "Prix Unitaire"])
            self.cart_items = []

            # Boutons
            self.create_order_button = QPushButton("Passer la Commande")
            self.cancel_button = QPushButton("Annuler")

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.create_order_button)
            button_layout.addWidget(self.cancel_button)

            # Connecter les boutons
            self.create_order_button.clicked.connect(self.confirm_create_order)
            self.cancel_button.clicked.connect(self.close)

            self.total_commande = 0
            self.panier_total = QLabel(f"Panier : {self.total_commande}$")

            # Agencer les widgets
            layout.addLayout(product_layout)
            layout.addLayout(quantity_layout)
            layout.addWidget(add_product_button)
            layout.addWidget(self.panier_total)
            layout.addWidget(self.cart_table)
            layout.addLayout(button_layout)

            self.setLayout(layout)

        def get_client_info(self):
            query = "SELECT * FROM Clients WHERE id_client = ?"
            result = self.db_manager.execute_query(query, (self.client_id,))
            if result:
                return result[0]
            else:
                return None

        def get_produits(self):
            query = "SELECT id_produit, nom_produit, prix FROM Produits"
            results = self.db_manager.execute_query(query)
            return results

        def add_product_to_cart(self):
            
            product_text = self.product_combo.currentText()
            product_id = int(product_text.split(' - ')[0])
            product_name = ' - '.join(product_text.split(' - ')[1:])
            quantity = self.quantity_input.value()

            # Récupérer le prix du produit
            query = "SELECT prix FROM Produits WHERE id_produit = ?"
            result = self.db_manager.execute_query(query, (product_id,))
            if result:
                prix_unitaire = result[0]['prix']
            else:
                QMessageBox.warning(self, "Erreur", "Produit non trouvé.")
                return
            
            self.total_commande += prix_unitaire
            self.prix_afficher = self.total_commande
            # regrde si les rabais s'applique
            for rabais in self.all_rabais:
                has_rabais = eval(f"{self.prix_afficher} {rabais.operateur} {rabais.value}")
                if has_rabais: 
                    self.prix_afficher -= self.prix_afficher * (rabais.rabais / 100)
                    
            if self.all_rabais: 
                self.panier_total.setText(f"Panier : { max(0,round((self.prix_afficher), 2)) }$")
            else : self.panier_total.setText(f"Panier : {self.total_commande}$")
            

            # Ajouter au panier
            self.cart_items.append({
                'id_produit': product_id,
                'nom_produit': product_name,
                'quantite': quantity,
                'prix_unitaire': prix_unitaire
            })

            self.update_cart_table()

        def update_cart_table(self):
            self.cart_table.setRowCount(0)
            for row_number, item in enumerate(self.cart_items):
                self.cart_table.insertRow(row_number)
                self.cart_table.setItem(row_number, 0, QTableWidgetItem(str(item['id_produit'])))
                self.cart_table.setItem(row_number, 1, QTableWidgetItem(item['nom_produit']))
                self.cart_table.setItem(row_number, 2, QTableWidgetItem(str(item['quantite'])))
                self.cart_table.setItem(row_number, 3, QTableWidgetItem(f"{item['prix_unitaire']:.2f}"))

        def confirm_create_order(self):
            if not self.cart_items:
                QMessageBox.warning(self, "Attention", "Votre panier est vide.")
                return

            try:
                # Calculer le total de la commande

                prix_final = self.total_commande
                for rabais in self.all_rabais:
                    has_rabais = eval(f"{prix_final} {rabais.operateur} {rabais.value}")
                    if has_rabais: 
                        prix_final -= prix_final * (rabais.rabais / 100)
                
                if self.all_rabais :  self.total_commande = max(0,round(prix_final,2))
                
                self.total_commande *= 1.15 #taxes
                
                # Insérer la commande
                query_commande = """
                INSERT INTO Commandes (id_client, date_commande, statut, total)
                VALUES (?, date('now'), ?, ?)
                """
                parameters_commande = (
                    self.client_id,
                    'En cours',
                    self.total_commande
                )
                self.db_manager.execute_update(query_commande, parameters_commande)
                id_commande = self.db_manager.cursor.lastrowid

                # Insérer les produits dans Commandes_Produits
                for item in self.cart_items:
                    query_produit_commande = """
                    INSERT INTO Commandes_Produits (id_commande, id_produit, quantite, prix_unitaire, total_ligne)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    total_ligne = item['quantite'] * item['prix_unitaire']
                    parameters_produit_commande = (
                        id_commande,
                        item['id_produit'],
                        item['quantite'],
                        item['prix_unitaire'],
                        total_ligne
                    )
                    self.db_manager.execute_update(query_produit_commande, parameters_produit_commande)

                # Émettre le signal
                self.order_created.emit({'id_commande': id_commande})
                QMessageBox.information(self, "Succès", "Commande créée avec succès.")
                self.close()

            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite lors de la création de la commande : {e}")

   