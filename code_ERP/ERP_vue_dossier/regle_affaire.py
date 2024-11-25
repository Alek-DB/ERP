from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from ERP_data_base import DatabaseManager
import re
import sqlite3

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
        layout.addWidget(QLabel("Gestion des Règles d'Affaires"))
        
        self.operateurs = {
            "<": "lt",
            "<=": "le",
            ">": "gt",
            ">=": "ge",
            "=": "eq",
            "!=": "ne"
        }
        
        # Création du formulaire pour la règle d'affaire
        form_layout = QGridLayout()

        # Choix de l'action
        self.combo_actions = QComboBox(self)
        self.combo_actions.addItem("Sélectionnez une action")
        self.combo_actions.addItem("Envoyer email")
        self.combo_actions.addItem("Appliquer rabais")
        form_layout.addWidget(QLabel("Action:"), 0, 0)
        form_layout.addWidget(self.combo_actions, 0, 1)
        
        # Sélection du champ de la table
        self.combo_champs = QComboBox(self)
        self.combo_champs.addItem("Sélectionnez un champ")
        self._charger_champs_table()  # Charger les champs depuis la base de données
        form_layout.addWidget(QLabel("Champ de Table:"), 1, 0)
        form_layout.addWidget(self.combo_champs, 1, 1)

        # Sélection de l'opérateur
        self.combo_operateurs = QComboBox(self)
        self.combo_operateurs.addItem("Sélectionnez un opérateur")
        for key, value in self.operateurs.items():
            self.combo_operateurs.addItem(key)
        form_layout.addWidget(QLabel("Opérateur:"), 2, 0)
        form_layout.addWidget(self.combo_operateurs, 2, 1)

        # Entrée de la donnée
        self.line_donnee = QLineEdit(self)
        self.line_donnee.setPlaceholderText("Entrez la donnée")
        form_layout.addWidget(QLabel("Valeur:"), 3, 0)
        form_layout.addWidget(self.line_donnee, 3, 1)

        # Nouveau champ de texte pour entrer une valeur à appliquer (email ou rabais)
        self.line_action_value = QLineEdit(self)
        self.line_action_value.setPlaceholderText("Entrez la valeur à appliquer (par exemple, texte pour email ou rabais)")
        form_layout.addWidget(QLabel("Texte à appliquer:"), 4, 0)
        form_layout.addWidget(self.line_action_value, 4, 1)
        
        # Nouveau champ de texte pour entrer une valeur à appliquer (email ou rabais)
        self.format = QLabel(self)
        self.format.setText("YYYY-MM-DD ou écrire naissance pour date de fête")
        self.format.setFixedHeight(20)
        form_layout.addWidget(QLabel("Format"), 5, 0)
        form_layout.addWidget(self.format, 5, 1)
        
        # Nouveau champ de texte pour entrer une valeur à appliquer (email ou rabais)
        self.date_edit = QLineEdit(self)
        self.date_edit.setPlaceholderText("Entrez la date")
        form_layout.addWidget(QLabel("Date"), 6, 0)
        form_layout.addWidget(self.date_edit, 6, 1)

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

    def basculer_before(self):
        """Méthode pour revenir à la page précédente (ou effectuer l'action associée au bouton retour)."""
        print("Retour à la page précédente.")
        self.close()

    def _charger_champs_table(self):
        """Charger dynamiquement les champs disponibles dans les tables depuis la base de données."""
        query = """
            SELECT name FROM sqlite_master WHERE type='table';
        """
        tables = self.db_manager.execute_query(query)  # Récupérer les noms des tables

        # Pour chaque table, récupérer les champs
        hidden = ["sqlite_sequence", "Regle_affaires", "Employes_Roles", "Employes_Succursales", "Fournisseurs_Produits", "Produits_Categories", "Commandes_Produits", "Achats_Produits", "Commandes_Promotions", ""]
        for table in tables:
            table_name = table[0]
            if table_name in hidden: continue
            query = f"PRAGMA table_info({table_name})"
            columns = self.db_manager.execute_query(query)  # Récupérer les colonnes de la table
            for column in columns:
                field_name = column[1]  # Nom du champ
                if "id_" in field_name: continue
                self.combo_champs.addItem(f"[{table_name}] - {field_name}")

    def mettre_a_jour_interface(self):
        """Mettre à jour l'interface en fonction de l'action choisie dans le QComboBox."""
        action = self.combo_actions.currentText()

        # Masquer ou afficher les champs en fonction de l'action
        if action == "Envoyer email":
            # Afficher les champs spécifiques à l'envoi d'email
            self.combo_champs.setEnabled(True)
            self.combo_operateurs.setCurrentText("=")  
            self.combo_operateurs.setEnabled(False)  # L'opérateur n'est pas nécessaire pour "Envoyer email"
            self.line_donnee.setEnabled(True)  # Pas besoin de valeur pour "Envoyer email"
            self.line_action_value.setPlaceholderText("Entrez le texte du message à envoyer par email")
            self.line_action_value.setEnabled(True)
            
            self.date_edit.setEnabled(True)
        elif action == "Appliquer rabais":
            # Afficher les champs spécifiques à l'application de rabais
            self.combo_champs.setEnabled(True)
            self.combo_operateurs.setEnabled(True)
            self.line_donnee.setEnabled(True)
            self.line_action_value.setPlaceholderText("Entrez le pourcentage du rabais à appliquer")
            self.line_action_value.setEnabled(True)
            
            self.date_edit.setEnabled(False)
        else:
            # Par défaut, on désactive tous les champs sauf la sélection de l'action
            self.combo_champs.setEnabled(False)
            self.combo_operateurs.setEnabled(False)
            self.line_donnee.setEnabled(False)
            self.line_action_value.setEnabled(False)
            
            self.date_edit.setEnabled(False)

    def enregistrer_regle(self):
        """Enregistrer la règle d'affaire dans la base de données."""
        champ_selectionne = self.combo_champs.currentText()
        operateur = self.combo_operateurs.currentText()
        valeur = self.line_donnee.text()
        action = self.combo_actions.currentText()
        desc = self.line_action_value.text()

        pattern = r"\[(.*?)\] - (.*)"
        match = re.match(pattern, champ_selectionne)
        table = match.group(1)
        champ = match.group(2)
        
        try:
            query = f"""
            INSERT INTO Regle_affaires (table_name, champ_name, operateur, valeur, action, desc)
            VALUES ("{table}", "{champ}", "{self.operateurs.get(operateur)}", "{valeur}", "{action}", "{desc}")
            """
            print(query)
            self.db_manager.execute_update(query, ())
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de l'enregistrement de la règle d'affaire : {e}")

        # Afficher un message de confirmation
        print(f"Règle d'affaire enregistrée : {champ_selectionne} {operateur} {valeur} -> {action} avec valeur {desc}")

    def envoyer_email(self, message):
        """Envoyer un email avec le texte passé en paramètre."""
        print(f"Email envoyé avec le message : {message}")

    def appliquer_rabais(self, rabais):
        """Appliquer un rabais à un produit ou une transaction."""
        print(f"Rabais de {rabais}% appliqué.")
