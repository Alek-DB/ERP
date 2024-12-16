from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from ERP_data_base import DatabaseManager
import re
import sqlite3
from ERP_vue_dossier.rabais import *
from datetime import datetime

class QRegleAffaire(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager('erp_database.db')  # Référence à votre db_manager
        
        # Initialisation du layout principal
        layout = QVBoxLayout(self)

        # Créer un bouton "Retour" en haut à gauche
        back_button = QPushButton("<-", self)
        back_button.clicked.connect(parent.basculer_before)  # Connecter au même slot qu'auparavant

        # Ajouter le bouton "Retour" au layout principal en haut
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Titre de la page
        layout.addWidget(QLabel("Gestion des Règles d'Affaires"), alignment=Qt.AlignCenter)
        btn = QPushButton("Afficher règles")
        btn.clicked.connect(parent.basculer_vers_afficher_regles_affaire)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        self.operateurs = ["<", "<=", ">", ">=", "=="]
        
        # Création du formulaire pour la règle d'affaire
        form_layout = QVBoxLayout()

        # Choix de l'action
        self.combo_actions = QComboBox(self)
        self.combo_actions.addItem("Sélectionnez une action")
        self.combo_actions.addItem("Envoyer email")
        self.combo_actions.addItem("Appliquer rabais")
        #self.combo_actions.addItem("Appliquer rabais")
        form_layout.addWidget(QLabel("Action:"))
        form_layout.addWidget(self.combo_actions)

        # Sélection du champ de la table
        self.combo_champs = QComboBox(self)
        self.combo_champs.addItem("Sélectionnez un champ")
        # self.email_table = ["Clients","Employes","Succursales","Fournisseurs"]
        # self.rabais_table = ["Clients","Succursales","Produits","Achats","Commandes"]
        
        self.champ_label = QLabel("Champ de Table:")
        form_layout.addWidget(self.champ_label)
        form_layout.addWidget(self.combo_champs)

        # Sélection de l'opérateur
        self.combo_operateurs = QComboBox(self)
        self.combo_operateurs.addItem("Sélectionnez un opérateur")
        for value in self.operateurs:
            self.combo_operateurs.addItem(value)
        self.operateur_label = QLabel("Opérateur:")
        form_layout.addWidget(self.operateur_label)
        form_layout.addWidget(self.combo_operateurs)

        # Entrée de la donnée
        self.line_donnee = QLineEdit(self)
        self.line_donnee.setPlaceholderText("Laisser vide pour sélectionner toute la table")
        self.valeur_label = QLabel("Valeur:")
        form_layout.addWidget(self.valeur_label)
        form_layout.addWidget(self.line_donnee)

        # Nouveau champ de texte pour entrer une valeur à appliquer (email ou rabais)
        self.line_action_value = QLineEdit(self)
        self.line_action_value.setPlaceholderText("Entrez la valeur à appliquer (par exemple, texte pour email ou rabais)")
        self.valeur_action_label = QLabel("Valeur Action:")
        form_layout.addWidget(self.valeur_action_label)
        form_layout.addWidget(self.line_action_value)

        # Format et Date (seulement affiché dans certains cas)
        self.format = QLabel(self)
        self.format.setText("YYYY-MM-DD / écrire naissance pour date de fête (juste pour Employés en Clients)")
        self.format.setFixedHeight(20)
        self.date_edit = QLineEdit(self)
        self.date_edit.setPlaceholderText("Entrez la date")
        self.format_label = QLabel("Format:")
        form_layout.addWidget(self.format_label)
        form_layout.addWidget(self.format)
        self.date_label = QLabel("Date:")
        form_layout.addWidget(self.date_label)
        form_layout.addWidget(self.date_edit)
        
        
        
        
        
        #RABAIS |||
        self.date_debut_rabais = QLineEdit(self)
        self.date_debut_rabais.setPlaceholderText("Entrez la date du début du rabais : YYYY-MM-DD")
        self.valeur_debut_label = QLabel("Date début:")
        form_layout.addWidget(self.valeur_debut_label)
        form_layout.addWidget(self.date_debut_rabais)
        
        self.date_fin_rabais = QLineEdit(self)
        self.date_fin_rabais.setPlaceholderText("Entrez la date de la fin du rabais : YYYY-MM-DD")
        self.valeur_fin_label = QLabel("Date fin:")
        form_layout.addWidget(self.valeur_fin_label)
        form_layout.addWidget(self.date_fin_rabais)
        
        

        # Ajouter le formulaire au layout principal
        layout.addLayout(form_layout)

        # Bouton pour enregistrer la règle d'affaire
        self.save_button = QPushButton("Enregistrer la Règle", self)
        self.save_button.clicked.connect(self.enregistrer_regle)
        layout.addWidget(self.save_button)

        # Connecter le changement de sélection dans le combo box d'actions
        self.combo_actions.currentIndexChanged.connect(self.mettre_a_jour_interface)

        # Initialiser l'interface avec la bonne configuration
        self.mettre_a_jour_interface()


    def _charger_champs_table(self, rabais):
        self.combo_champs.clear()
        if rabais:
            self.combo_champs.addItem(f"[Commandes] - total")
        else:
            self.combo_champs.addItem(f"[Employes] - id_employe")
            self.combo_champs.addItem(f"[Succursales] - id_succursale")
            self.combo_champs.addItem(f"[Clients] - id_client")
            self.combo_champs.addItem(f"[Fournisseurs] - id_fournisseur")
            
        # """Charger dynamiquement les champs disponibles dans les tables depuis la base de données."""
        # query = """
        #     SELECT name FROM sqlite_master WHERE type='table';
        # """
        # tables = self.db_manager.execute_query(query)  # Récupérer les noms des tables

        # self.combo_champs.clear()
        # # Pour chaque table, récupérer les champs
        # for table in tables:
        #     table_name = table[0]
        #     if table_name not in show: continue
        #     query = f"PRAGMA table_info({table_name})"
        #     columns = self.db_manager.execute_query(query)  # Récupérer les colonnes de la table
        #     for column in columns:
        #         field_name = column[1]  # Nom du champ
        #         if "id_" in field_name: continue
        #         self.combo_champs.addItem(f"[{table_name}] - {field_name}")

    def mettre_a_jour_interface(self):
        """Mettre à jour l'interface en fonction de l'action choisie dans le QComboBox."""
        action = self.combo_actions.currentText()

        # Masquer ou afficher les champs en fonction de l'action
        if action == "Envoyer email":
            # Afficher les champs spécifiques à l'envoi d'email
            self._charger_champs_table(False )  # Charger les champs depuis la base de données
            self.champ_label.setVisible(True)
            self.operateur_label.setVisible(True)
            self.combo_champs.setVisible(True)
            self.combo_operateurs.setVisible(True)
            self.combo_operateurs.setCurrentText("==")
            self.combo_operateurs.setEnabled(False)  # L'opérateur n'est pas nécessaire pour "Envoyer email"
            
            #valeur
            self.valeur_label.setVisible(True)
            self.valeur_action_label.setVisible(True)
            self.line_action_value.setPlaceholderText("Entrez le texte du message à envoyer par email")
            self.line_donnee.setVisible(True)
            self.line_donnee.setPlaceholderText("Laisser vide pour sélectionner toute la table")
            self.line_action_value.setVisible(True)

            #format date
            self.format_label.setVisible(True)
            self.format.setVisible(True)
            self.date_label.setVisible(True)
            self.date_edit.setVisible(True)
            
            
            #date
            self.date_debut_rabais.setVisible(False)
            self.valeur_debut_label.setVisible(False)
            self.date_fin_rabais.setVisible(False)
            self.valeur_fin_label.setVisible(False)
            
        elif action == "Appliquer rabais":
            # Afficher les champs spécifiques à l'application de rabais
            self._charger_champs_table(True )  # Charger les champs depuis la base de données
            self.champ_label.setVisible(True)
            self.operateur_label.setVisible(True)
            self.combo_champs.setVisible(True)
            self.combo_operateurs.setVisible(True)
            self.combo_operateurs.setEnabled(True)
            
            #valeur
            self.valeur_label.setVisible(True)
            self.valeur_action_label.setVisible(True)
            self.line_action_value.setPlaceholderText("Entrez le pourcentage du rabais à appliquer ex: 50 pour 50%")
            self.line_donnee.setVisible(True)
            self.line_donnee.setPlaceholderText("Entrez la valeur")
            self.line_action_value.setVisible(True)
            
            #format date
            self.format_label.setVisible(False)
            self.format.setVisible(False)
            self.date_label.setVisible(False)
            self.date_edit.setVisible(False)
            
            #date
            self.date_debut_rabais.setVisible(True)
            self.valeur_debut_label.setVisible(True)
            self.date_fin_rabais.setVisible(True)
            self.valeur_fin_label.setVisible(True)
        else:
            # Par défaut, on désactive tous les champs sauf la sélection de l'action
            self.champ_label.setVisible(False)
            self.operateur_label.setVisible(False)
            self.combo_champs.setVisible(False)
            self.combo_operateurs.setVisible(False)
            
            #valeur
            self.valeur_label.setVisible(False)
            self.valeur_action_label.setVisible(False)
            self.line_donnee.setVisible(False)
            self.line_action_value.setVisible(False)
            
            #format date
            self.format_label.setVisible(False)
            self.format.setVisible(False)
            self.date_label.setVisible(False)
            self.date_edit.setVisible(False)
            
            #date
            self.date_debut_rabais.setVisible(False)
            self.valeur_debut_label.setVisible(False)
            self.date_fin_rabais.setVisible(False)
            self.valeur_fin_label.setVisible(False)

    def enregistrer_regle(self):
        """Enregistrer la règle d'affaire dans la base de données."""
        champ_selectionne = self.combo_champs.currentText()
        operateur = self.combo_operateurs.currentText()
        valeur = self.line_donnee.text()
        action = self.combo_actions.currentText()
        desc = self.line_action_value.text()
        date = self.date_edit.text()
        date_debut = self.date_debut_rabais.text()
        date_fin = self.date_fin_rabais.text()
        
        pattern = r"\[(.*?)\] - (.*)"
        match = re.match(pattern, champ_selectionne)
        table = match.group(1)
        champ = match.group(2)
    
        #errors
        if valeur == "" and action == "Envoyer email" and table not in ["Employes", "Clients"]:
            QMessageBox.critical(None, "Erreur", f"Valeur vide mais table n'est pas Clients ou Employés")
            return
        
        if action == "Envoyer email":
            try:
                if date != "naissance":
                    date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                QMessageBox.critical(None, "Erreur", f"La date n'est pas du bon format")
                return
    

        if action == "Appliquer rabais":
            try: 
                float(valeur)
                float(desc)
            except:
                QMessageBox.critical(None, "Erreur", f"L'une de vos valeur n'est pas un nombre")
                return
            try:
                date = datetime.strptime(date_debut, "%Y-%m-%d")
                date = datetime.strptime(date_fin, "%Y-%m-%d")
            except ValueError:
                QMessageBox.critical(None, "Erreur", f"Une des dates n'est pas du bon format")
                return
            
        if self.combo_operateurs.currentText() == "Sélectionnez un opérateur":
            QMessageBox.critical(None, "Erreur", f"Veuillez choisir un opérateur")
            return

        try:
            if action == "Envoyer email":
            # si j'envoi un email a tout mes employés ou clients, faire plusieurs regles d'affaire
                if valeur == "": # toute les valeurs de la table
                    all_element = self.db_manager.execute_query(f"SELECT * FROM {table}", ())
                    for element in all_element:
                        status = "pending"
                        date_msg = date
                        if table == "Employes":
                            if date == "naissance":
                                date_msg = element[6]
                                status = "infinite"
                                
                            query = f"""
                            INSERT INTO Regle_affaires (table_name, champ_name, operateur, valeur, action, desc, date_send, statut)
                            VALUES ("{table}", "id_employe", "{operateur}", "{element[0]}", "{action}", "{desc}", "{date_msg}", "{status}")
                            """
                        elif table == "Clients":
                            if date == "naissance":
                                date_msg = element[5]
                                status = "infinite"
                            query = f"""
                            INSERT INTO Regle_affaires (table_name, champ_name, operateur, valeur, action, desc, date_send, statut)
                            VALUES ("{table}", "id_client", "{operateur}", "{element[0]}", "{action}", "{desc}", "{date_msg}", "{status}")
                            """
                        self.db_manager.execute_update(query, ())
                else:
                    # sinon crée juste une regle
                    query = f"""
                    INSERT INTO Regle_affaires (table_name, champ_name, operateur, valeur, action, desc, date_send, statut)
                    VALUES ("{table}", "{champ}", "{operateur}", "{valeur}", "{action}", "{desc}", "{date}", "pending")
                    """
            elif action == "Appliquer rabais":
                query =f"""
                    INSERT INTO Regle_affaires (table_name, champ_name, operateur, valeur, action, desc,  date_debut, date_fin, statut)
                    VALUES ("{table}", "{champ}", "{operateur}", "{valeur}", "{action}", "{desc}", "{date_debut}", "{date_fin}" ,"pending")
                    """
                
            QMessageBox.information(None, "", f"Votre règle à été enregistré")
            self.db_manager.execute_update(query, ())
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de l'enregistrement de la règle d'affaire : {e}")
