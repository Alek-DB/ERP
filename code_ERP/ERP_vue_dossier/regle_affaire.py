from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from ERP_data_base import DatabaseManager

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

        # Création du formulaire pour la règle d'affaire
        form_layout = QGridLayout()

        # Sélection du champ de la table
        self.combo_champs = QComboBox(self)
        self.combo_champs.addItem("Sélectionnez un champ")
        self._charger_champs_table()  # Charger les champs depuis la base de données
        form_layout.addWidget(QLabel("Champ de Table:"), 0, 0)
        form_layout.addWidget(self.combo_champs, 0, 1)

        # Sélection de l'opérateur
        self.combo_operateurs = QComboBox(self)
        self.combo_operateurs.addItem("Sélectionnez un opérateur")
        self.combo_operateurs.addItem("<")
        self.combo_operateurs.addItem("<=")
        self.combo_operateurs.addItem(">")
        self.combo_operateurs.addItem(">=")
        self.combo_operateurs.addItem("=")
        self.combo_operateurs.addItem("!=")
        form_layout.addWidget(QLabel("Opérateur:"), 1, 0)
        form_layout.addWidget(self.combo_operateurs, 1, 1)

        # Entrée de la donnée
        self.line_donnee = QLineEdit(self)
        self.line_donnee.setPlaceholderText("Entrez la donnée")
        form_layout.addWidget(QLabel("Valeur:"), 2, 0)
        form_layout.addWidget(self.line_donnee, 2, 1)

        # Choix de l'action
        self.combo_actions = QComboBox(self)
        self.combo_actions.addItem("Sélectionnez une action")
        self.combo_actions.addItem("Envoyer email")
        self.combo_actions.addItem("Appliquer rabais")
        form_layout.addWidget(QLabel("Action:"), 3, 0)
        form_layout.addWidget(self.combo_actions, 3, 1)

        # Nouveau champ de texte pour entrer une valeur à appliquer (email ou rabais)
        self.line_action_value = QLineEdit(self)
        self.line_action_value.setPlaceholderText("Entrez la valeur à appliquer (par exemple, texte pour email ou rabais)")
        form_layout.addWidget(QLabel("Texte à appliquer:"), 4, 0)
        form_layout.addWidget(self.line_action_value, 4, 1)

        # Ajouter le formulaire au layout principal
        layout.addLayout(form_layout)

        # Bouton pour enregistrer la règle d'affaire
        self.save_button = QPushButton("Enregistrer la Règle", self)
        self.save_button.clicked.connect(self.enregistrer_regle)
        layout.addWidget(self.save_button)

    def basculer_before(self):
        """Méthode pour revenir à la page précédente (ou effectuer l'action associée au bouton retour)."""
        # Implémenter la logique pour revenir à la page précédente ou effectuer une autre action
        print("Retour à la page précédente.")
        # Par exemple : vous pouvez utiliser `self.close()` ou toute autre logique selon votre structure d'interface
        self.close()

    def _charger_champs_table(self):
        """Charger dynamiquement les champs disponibles dans les tables depuis la base de données."""
        query = """
            SELECT name FROM sqlite_master WHERE type='table';
        """
        tables = self.db_manager.execute_query(query)  # Récupérer les noms des tables

        # Pour chaque table, récupérer les champs
        for table in tables:
            table_name = table[0]
            query = f"PRAGMA table_info({table_name})"
            columns = self.db_manager.execute_query(query)  # Récupérer les colonnes de la table
            for column in columns:
                field_name = column[1]  # Nom du champ
                self.combo_champs.addItem(f"{table_name}.{field_name}")

    def enregistrer_regle(self):
        """Enregistrer la règle d'affaire dans la base de données."""
        champ_selectionne = self.combo_champs.currentText()
        operateur_selectionne = self.combo_operateurs.currentText()
        valeur_donnee = self.line_donnee.text()
        action_selectionnee = self.combo_actions.currentText()
        valeur_action = self.line_action_value.text()

        # Vérification des champs obligatoires
        if champ_selectionne == "Sélectionnez un champ" or operateur_selectionne == "Sélectionnez un opérateur" or valeur_donnee == "" or action_selectionnee == "Sélectionnez une action" or valeur_action == "":
            print("Veuillez remplir tous les champs.")
            return

        # Exécuter la logique selon l'action sélectionnée
        if action_selectionnee == "Envoyer email":
            self.envoyer_email(valeur_action)
        elif action_selectionnee == "Appliquer rabais":
            self.appliquer_rabais(valeur_action)

        # Afficher un message de confirmation
        print(f"Règle d'affaire enregistrée : {champ_selectionne} {operateur_selectionne} {valeur_donnee} -> {action_selectionnee} avec valeur {valeur_action}")

    def envoyer_email(self, message):
        """Envoyer un email avec le texte passé en paramètre."""
        # Implémentation de l'envoi d'email ici
        print(f"Email envoyé avec le message : {message}")

    def appliquer_rabais(self, rabais):
        """Appliquer un rabais à un produit ou une transaction."""
        # Implémentation de l'application du rabais ici
        print(f"Rabais de {rabais}% appliqué.")
