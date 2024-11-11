import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QComboBox
)
import sqlite3
from PySide6.QtCore import Qt
from ERP_data_base import DatabaseManager

class QAjoutChamp(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        self.setWindowTitle("Ajout Champ")
        self.setGeometry(100, 100, 800, 400)

        self.mode = ""  # Variable pour stocker le mode

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout pour les boutons
        button_layout = QVBoxLayout()
        
        # Bouton retour en haut
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        button_layout.addWidget(back_button)

        # Liste des noms de boutons
        button_names = ["Produits", "Employes", "Clients", "Succursales", "Fournisseurs"]
        self.buttons = {}

        # Création des boutons avec un espacement réduit
        for name in button_names:
            button = QPushButton(name)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, btn=button: self.on_button_clicked(btn))
            self.buttons[name] = button
            button_layout.addWidget(button)
            button_layout.setSpacing(5)  # Espacement entre les boutons

        # Mise en vert du bouton "Produits" et assignation du mode
        self.buttons["Produits"].setStyleSheet("background-color: lightgreen;")
        self.mode = "Produits"

        # Layout pour les champs texte
        fields_layout = QHBoxLayout()
        
        # Champ "Nom du champ"
        nom_layout = QVBoxLayout()
        self.label_nom = QLabel("Nom du champ:")
        self.input_nom = QLineEdit()
        nom_layout.addWidget(self.label_nom)
        nom_layout.addWidget(self.input_nom)

        # Champ "Type de données" avec un menu déroulant
        type_layout = QVBoxLayout()
        self.label_type = QLabel("Type de données:")
        self.input_type = QComboBox()
        
        # Liste des types de données SQLite
        sqlite_data_types = [
            "INTEGER", "REAL", "TEXT", "BLOB", "NUMERIC"
        ]
        self.input_type.addItems(sqlite_data_types)
        
        type_layout.addWidget(self.label_type)
        type_layout.addWidget(self.input_type)

        # Bouton pour ajouter le champ
        self.ajout_btn = QPushButton("Ajouter le champ")
        self.ajout_btn.clicked.connect(self.ajouter)

        # Ajout des deux layouts dans le layout horizontal
        fields_layout.addLayout(nom_layout)
        fields_layout.addLayout(type_layout)
        fields_layout.addWidget(self.ajout_btn)

        # Centrer le layout des champs
        fields_layout.setAlignment(Qt.AlignCenter)

        # Ajout de padding autour du regroupement
        for layout in (nom_layout, type_layout):
            layout.setContentsMargins(10, 10, 10, 10)  # Padding autour des layouts

        # Ajout du layout des champs à droite
        right_layout = QVBoxLayout()
        right_layout.addLayout(fields_layout)
        right_layout.setAlignment(Qt.AlignCenter)

        # Ajout des layouts au layout principal
        main_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def on_button_clicked(self, button):
        # Réinitialise les autres boutons
        for btn in self.buttons.values():
            if btn != button:
                btn.setChecked(False)
                btn.setStyleSheet("")
            else:
                btn.setStyleSheet("background-color: lightgreen;")  # Couleur de fond du bouton sélectionné
                self.mode = button.text()  # Mettre à jour le mode avec le texte du bouton

    def ajouter(self):
        
        # Vérifiez que les champs sont remplis
        if self.input_nom.text() != "" and self.input_type.currentText() != "":
            nom_table = self.mode
            nom_new_champ = self.input_nom.text()
            type_new_champ = self.input_type.currentText()
            db_manager = DatabaseManager('erp_database.db')
            query = f"ALTER TABLE {nom_table} ADD COLUMN {nom_new_champ} {type_new_champ};"
            try:
                # Exécution de la requête
                db_manager.execute_update(query)
                print(f"Colonne '{nom_new_champ}' ajoutée à la table '{nom_table}'.")
            except sqlite3.Error as e:
                print(f"Erreur lors de l'ajout de la colonne : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QAjoutChamp()
    window.show()
    sys.exit(app.exec())
