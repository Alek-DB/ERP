import sys
import sqlite3
from PySide6.QtWidgets import (
<<<<<<< HEAD
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel
=======
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QComboBox,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QDialog, QMessageBox
>>>>>>> a52582001cd5d8ae733eb36818ecd9b2d2e3b712
)
from PySide6.QtCore import Qt

from ERP_data_base import DatabaseManager

<<<<<<< HEAD
class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.vue = parent

        # Titre de la fenêtre
        self.setWindowTitle("Page Succursale")

        # Initialiser le mode à aucun
        self.current_mode = None

        # Création des boutons
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.vue.basculer_vers_gerant_global)
        ajouter_button = QPushButton("Ajouter")
        ajouter_button.clicked.connect(lambda: self.vue.basculer_vers_ajout_succursale(True))
        modifier_button = QPushButton("Modifier")
        retirer_button = QPushButton("Retirer")

        # Connecter les boutons à leurs actions respectives
        modifier_button.clicked.connect(lambda: self.set_mode('modifier'))
        retirer_button.clicked.connect(lambda: self.set_mode('retirer'))

        # Mise en page principale
        main_layout = QHBoxLayout()  # Utiliser un layout horizontal

        # Mise en page pour tous les boutons
        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button, alignment=Qt.AlignTop)  # Bouton Back en haut

        # Espacement pour centrer les autres boutons
        button_layout.addStretch()  # Ajout d'un étirement pour espacer le bouton Back des autres
        button_layout.addWidget(ajouter_button)
        button_layout.addWidget(modifier_button)
        button_layout.addWidget(retirer_button)
        button_layout.addStretch()  # Ajout d'un étirement pour espacer le bouton Back des autres

        # Ajouter du padding entre les boutons
        button_layout.setSpacing(10)  # Espacement entre les boutons
        button_layout.setAlignment(Qt.AlignLeft)  # Aligner à gauche

        # Ajouter le layout des boutons au layout principal
        main_layout.addLayout(button_layout)

        # Ajout d'un espace flexible pour pousser la QListe à droite
        main_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))



        section_names = ["Nom", "Adresse", "Code"]  # Exemple de noms de sections
        
        layout_list = []

        # db_manager = DatabaseManager('erp_database.db')
        # query = "SELECT * FROM Succursales"
        # results = db_manager.execute_query(query, (1,))

        # for row in results:
        #     _nom = row['nom']
        #     _adresse = row['adresse']
        #     _code = row["code"]
            
        #     layout_obj = []
        #     nom = QPushButton(_nom)
        #     nom.clicked.connect(self.handle_button_click)
        #     layout_obj.append(nom)
            
        #     addresse = QLabel(_adresse)
        #     layout_obj.append(addresse)
            
        #     _code = QLabel("5")
        #     layout_obj.append(_code)
            
        #     layout_list.append(layout_obj) 
        # liste = QListe("Liste de succursale", layout_list, section_names)
        # main_layout.addWidget(liste, alignment=Qt.AlignCenter)  

        self.setLayout(main_layout)

    def set_mode(self, mode):
        self.current_mode = mode
        for btn in self.findChildren(QPushButton):
            if btn.text() == "Modifier":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'modifier' else "background-color: lightblue;")
            elif btn.text() == "Retirer":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'retirer' else "background-color: lightcoral;")

    def handle_button_click(self):
        if self.current_mode == 'modifier':
            self.vue.basculer_vers_ajout_succursale(False)
        elif self.current_mode == 'retirer':
            print("Mode Retirer activé.")
            ## retirer dans la base de données
        else:
            self.vue.afficher_message("Selectionner", "Veuillez sélectionner un mode")
=======

class AddModifyDialog(QDialog):
    def __init__(self, parent, mode="Ajouter", product_data=None):
        super().__init__()
        
        self.succursale = parent
        self.mode = mode
        self.product_data = product_data
        
 
        self.setWindowTitle(self.mode)
        # Create the layout
        layout = QGridLayout()

        # prend le nom des tables
        labels = []
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT * FROM Succursales"
            db_manager.execute_query(query, ())
            labels = db_manager.get_column_names()
            labels.remove("date_ouverture")
            labels.remove("id_succursale")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
            
        self.inputs = {}

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if label == "statut":
                # Créer un QComboBox pour le champ Statut
                input_field = QComboBox()
                input_field.addItems(["Actif", "Fermé"])  # Options du dropdown
            else:
                input_field = QLineEdit()  # Champ texte pour les autres labels
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label] = input_field

        # Buttons for 'Ajouter/Modifier' and 'Annuler'
        self.add_modify_button = QPushButton(self.mode)
        self.cancel_button = QPushButton("Annuler")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)
        
        
        if self.mode == "Modifier" and self.product_data:
            self.fill_inputs()

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        if self.mode == "Ajouter":
            self.add_modify_button.clicked.connect(self.enregistrer)
        else:
            self.add_modify_button.clicked.connect(self.modify_product)
        
        
    def fill_inputs(self):
        if self.product_data:
            self.inputs["nom"].setText(self.product_data['nom'])
            self.inputs["adresse"].setText(self.product_data['adresse'])
            self.inputs["code"].setText(str(self.product_data['code']))
            self.inputs["gerant"].setText(str(self.product_data['gerant']))
            self.inputs["statut"].setCurrentText(str(self.product_data['statut']))
            self.inputs["telephone"].setText(str(self.product_data['telephone']))

    
    def modify_product(self):
        # Récupérer les valeurs des champs de saisie
        nom = self.inputs["nom"].text()
        code_succursale = self.inputs["code"].text()
        adresse = self.inputs["adresse"].text()
        gerant = self.inputs["gerant"].text()
        statut = self.inputs["statut"].currentText()
        telephone = self.inputs["telephone"].text()

        # Vérifier que tous les champs sont remplis
        if not (nom and code_succursale and adresse and gerant and statut and telephone):
            print("Tous les champs doivent être remplis.")
            return

        # Appeler la méthode de la classe parente pour mettre à jour les données
        self.succursale.update_product(self.product_data['code'], nom, code_succursale, adresse, gerant, statut, telephone)
        self.close()
    
    def enregistrer(self):
        """Récupérer les valeurs des champs et les enregistrer dans la base de données."""
        values = {
            label: input_field.currentText() if isinstance(input_field, QComboBox) else input_field.text() 
            for label, input_field in self.inputs.items()
        }

        try: 
            db_manager = DatabaseManager('erp_database.db')
            
            # Construire la requête dynamiquement
            columns = ', '.join(values.keys())  # Clés du dictionnaire
            placeholders = ', '.join(['?'] * (len(values)))  # Des points d'interrogation pour les valeurs


            query = f"""
            INSERT INTO Succursales ({columns}, date_ouverture)
            VALUES ({placeholders}, date('now'))
            """

            # Récupérer les valeurs dans l'ordre des colonnes
            parameters = list(values.values()) 

            rows_affected = db_manager.execute_update(query, parameters)

            if rows_affected > 0:
                print("La succursale a été ajouté avec succès.")
                self.succursale.load_succursale()
            else:
                print("Aucune ligne n'a été ajoutée.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
        
        self.close()
        
        
        
class QSuccursale(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        #set database
        self.db_manager = DatabaseManager('erp_database.db')

        # Create the main layout
        succursale_layout = QGridLayout()

        # Left-side buttons layout (Ajouter, Retirer, Modifier, etc.)
        add_button = QPushButton("Ajouter")
        remove_button = QPushButton("Retirer")
        modify_button = QPushButton("Modifier")
        back_button = QPushButton("<-")

        button_layout = QVBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(modify_button)

        # Add button layout to the grid
        succursale_layout.addLayout(button_layout, 0, 0)

        # Title of the inventory
        title_label = QLabel("Succursales")
        title_label.setAlignment(Qt.AlignCenter)
        succursale_layout.addWidget(title_label, 0, 1)

        # Search bar
        search_label = QLabel("Rechercher :")
        search_input = QLineEdit()

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        succursale_layout.addLayout(search_layout, 1, 1)

        self.succursale_table = QTableWidget()
        self.succursale_table.setColumnCount(7)
        self.setLayout(succursale_layout)
        self.load_succursale()

        # Add table to layout
        succursale_layout.addWidget(self.succursale_table, 2, 1)

        # Set central widget
    

        # Connect button actions to methods
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)
        modify_button.clicked.connect(self.modify_item)
        back_button.clicked.connect(parent.basculer_vers_gerant_global)
             
    def load_succursale(self):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT nom, adresse, code, gerant, statut, telephone, date_ouverture FROM Succursales"
            rows = db_manager.execute_query(query, ())
            self.succursale_table.setHorizontalHeaderLabels(["Nom", "Adresse", "Code", "Gerant", "Statut", "Telephone", "Date d'Ouverture"])

            self.succursale_table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.succursale_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

    def add_item(self):
        # Open the Add/Modify dialog
        dialog = AddModifyDialog(self)
        dialog.exec_()
        
    def remove_item(self):
        self.succursale_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.succursale_table.setSelectionMode(QTableWidget.SingleSelection)
        self.succursale_table.itemClicked.connect(self.confirm_deletion)

    def confirm_deletion(self, item):
        """Demander confirmation avant de supprimer un élément."""
        # Obtenir la ligne de l'élément sélectionné
        row = item.row()

        nom_succursale = self.succursale_table.item(row, 0).text()
        code_succursale = self.succursale_table.item(row, 2).text()

        # Boîte de dialogue de confirmation
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Confirmer la suppression")
        confirmation_dialog.setText(f"Voulez-vous vraiment supprimer la succursale '{nom_succursale}' (Code: {code_succursale}) ?")
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setIcon(QMessageBox.Warning)

        # Si l'utilisateur confirme la suppression
        if confirmation_dialog.exec_() == QMessageBox.Yes:
            self.delete_succursale(code_succursale)
        else:
            # Annuler la sélection si l'utilisateur ne veut pas supprimer
            self.succursale_table.clearSelection()

        # Désactiver la connexion à l'événement après la suppression ou l'annulation
        self.succursale_table.itemClicked.disconnect()
        self.load_succursale()

    def delete_succursale(self, code_succursale):
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "DELETE FROM Succursales WHERE code = ?"
            db_manager.execute_query(query, (code_succursale,))

            print(f"La succursale avec le code {code_succursale} a été supprimé.")
        except Exception as e:
            print(f"Erreur lors de la suppression de la succursale: {e}") 

    def modify_item(self):
        self.succursale_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.succursale_table.setSelectionMode(QTableWidget.SingleSelection)
        self.succursale_table.itemClicked.connect(self.open_modify_dialog)
        
    def open_modify_dialog(self, item):
        row = item.row()
        
        product_data = {
            'nom': self.succursale_table.item(row, 0).text(),
            'adresse': self.succursale_table.item(row, 1).text(),
            'code': self.succursale_table.item(row, 2).text(),
            'gerant': self.succursale_table.item(row, 3).text(),
            'statut': self.succursale_table.item(row, 4).text(),
            'telephone': self.succursale_table.item(row, 5).text(),
            'date_ouverture': self.succursale_table.item(row, 6).text()
        }

        # Ouvrir le dialogue en mode modification
        dialog = AddModifyDialog(self, mode="Modifier", product_data=product_data)
        dialog.exec_()
       

    def update_product(self, old_code_succursale, nom, new_code_succursale, adresse, gerant, statut, telephone):

            try:
                self.db_manager.execute_update("""
                    UPDATE Succursales
                    SET nom = ?, code = ?, adresse = ?, gerant = ?, statut = ?, telephone = ?
                    WHERE code = ?
                """, (nom, new_code_succursale, adresse, gerant, statut, telephone, old_code_succursale))

                self.load_succursale()


                print(f"Succursale {nom} mis à jour avec succès.")
            except Exception as e:
                print(f"Erreur lors de la mise à jour de la succursale: {e}")

>>>>>>> a52582001cd5d8ae733eb36818ecd9b2d2e3b712
