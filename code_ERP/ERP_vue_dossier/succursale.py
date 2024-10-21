from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QGridLayout, QLineEdit, QDialog, QComboBox
)
from PySide6.QtCore import Qt

from utils.QListe import QListe
from ERP_data_base import DatabaseManager

import sqlite3

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
        ajouter_button.clicked.connect(self.ajout)
        modifier_button = QPushButton("Modifier")
        retirer_button = QPushButton("Retirer")

        # Connecter les boutons à leurs actions respectives
        modifier_button.clicked.connect(lambda: self.set_mode('modifier'))
        retirer_button.clicked.connect(lambda: self.set_mode('retirer'))

        # Mise en page principale
        self.main_layout = QHBoxLayout()  # Utiliser un layout horizontal

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
        self.main_layout.addLayout(button_layout)

        # Ajout d'un espace flexible pour pousser la QListe à droite
        self.main_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.liste_widget = None
        self.refresh_liste() 
        self.setLayout(self.main_layout)

    def set_mode(self, mode):
        self.current_mode = mode
        for btn in self.findChildren(QPushButton):
            if btn.text() == "Modifier":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'modifier' else "background-color: lightblue;")
            elif btn.text() == "Retirer":
                btn.setStyleSheet("background-color: lightgray;" if mode != 'retirer' else "background-color: lightcoral;")

    def handle_button_click(self):
        if self.current_mode == 'modifier':
            dialog = AddModifyDialog(self)
            dialog.exec_()
        elif self.current_mode == 'retirer':
            print("Mode Retirer activé.")
            ## retirer dans la base de données
        else:
            self.vue.afficher_message("Selectionner", "Veuillez sélectionner un mode")
        
    def ajout(self):
        dialog = AddModifyDialog(self)
        dialog.exec_()
        
    def refresh_liste(self):
        """Met à jour la liste des succursales."""
        if self.liste_widget:
            self.liste_widget.deleteLater()  # Supprime l'ancienne liste

        layout_list = []
        section_names = ["Nom", "Adresse", "Code"]

        try:
            db_manager = DatabaseManager('erp_database.db')
            query = "SELECT * FROM Succursales"
            results = db_manager.execute_query(query, ())
            print(results.count)

            for row in results:
                _nom = row['nom']
                _adresse = row['adresse']
                _code = row["code"]

                layout_obj = []
                nom_button = QPushButton(_nom)
                nom_button.clicked.connect(self.handle_button_click)
                layout_obj.append(nom_button)

                addresse_label = QLabel(_adresse)
                layout_obj.append(addresse_label)

                code_label = QLabel(_code)
                layout_obj.append(code_label)

                layout_list.append(layout_obj)

            self.liste_widget = QListe("Liste de succursale", layout_list, section_names)
        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")

        self.main_layout.addWidget(self.liste_widget, alignment=Qt.AlignCenter)
        
        





class AddModifyDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.succursale = parent
        
        #CREER UN EMPLOYÉ
        db_manager = DatabaseManager('erp_database.db')
        try:
            # Vérifier si la table est vide
            check_query = "SELECT COUNT(*) FROM Employes"
            result = db_manager.execute_query(check_query)
            count = result[0][0]  # Récupérer le nombre d'employés

            if count == 0:
                # Ajouter un nouvel employé
                insert_query = """
                INSERT INTO Employes (nom, prenom, poste) VALUES (?, ?, ?)
                """
                parameters = ("Dupont", "Jean", "Développeur")  # Remplacez par les valeurs souhaitées
                rows_affected = db_manager.execute_update(insert_query, parameters)

                if rows_affected > 0:
                    print("Un nouvel employé a été ajouté avec succès.")
                else:
                    print("Aucun employé n'a été ajouté.")
            else:
                print("La table n'est pas vide. Aucun employé n'a été ajouté.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {type(e).__name__} - {e}")
        
        
        
        
        
        
        
        self.setWindowTitle("Ajouter")
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
        self.add_modify_button = QPushButton("Ajouter")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_modify_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout, len(labels), 1)

        # Set the layout
        self.setLayout(layout)

        # Connect cancel button to close the dialog
        self.cancel_button.clicked.connect(self.close)
        self.add_modify_button.clicked.connect(self.enregistrer)
        
        
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
            else:
                print("Aucune ligne n'a été ajoutée.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue : {e}")
        
        self.succursale.refresh_liste()
        self.close()
        
        


        




