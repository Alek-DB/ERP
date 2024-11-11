import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTimeEdit, QPushButton, QComboBox, QGridLayout
from PySide6.QtGui import QIntValidator


from ERP_data_base import DatabaseManager
from ERP_emplacement import Emplacement

class QHoraire(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        """Initialisation de l'interface utilisateur."""
        layout = QVBoxLayout(self)
        
        # Titre
        layout.addWidget(QLabel("Gestion des Horaires"))

        # Création du formulaire pour les horaires de chaque jour de la semaine
        grid_layout = QGridLayout()
        self.inputs = {}

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

        for i, jour in enumerate(jours):
            # Labels pour chaque jour
            grid_layout.addWidget(QLabel(jour), i, 0)

            # Champs pour l'heure d'entrée et l'heure de sortie
            heure_entree = QTimeEdit(self)
            heure_sortie = QTimeEdit(self)

            # Ajouter les widgets à la grille
            grid_layout.addWidget(heure_entree, i, 1)
            grid_layout.addWidget(heure_sortie, i, 2)

            # Stocker ces champs dans un dictionnaire
            self.inputs[f'heure_entree_{jour.lower()}'] = heure_entree
            self.inputs[f'heure_sortie_{jour.lower()}'] = heure_sortie

        # Bouton pour enregistrer les horaires
        save_button = QPushButton("Enregistrer", self)
        save_button.clicked.connect(self.save_horaire)
        
        layout.addLayout(grid_layout)
        layout.addWidget(save_button)

    def load_horaires(self):
        """Récupérer les horaires de l'employé et de la succursale depuis la base de données et les afficher."""
        try:
            db_manager = DatabaseManager('erp_database.db')

            # Récupérer l'horaire de l'employé pour cette succursale
            query = """
                SELECT heure_entree_lundi, heure_sortie_lundi,
                       heure_entree_mardi, heure_sortie_mardi,
                       heure_entree_mercredi, heure_sortie_mercredi,
                       heure_entree_jeudi, heure_sortie_jeudi,
                       heure_entree_vendredi, heure_sortie_vendredi
                FROM Horaires
                WHERE id_employe = ? AND id_succursale = ?
            """
            result = db_manager.execute_query(query, (Emplacement.employeHoraire, Emplacement.succursalesId))

            if result:
                horaires = result[0]
                print(horaires[0])
                jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]

                # Remplir les champs de l'interface avec les horaires récupérés
                for i, jour in enumerate(jours):
                    self.inputs[f'heure_entree_{jour}'].setTime(horaires[i*2])  # Heure d'entrée
                    self.inputs[f'heure_sortie_{jour}'].setTime(horaires[i*2 + 1])  # Heure de sortie
            else:
                print("Aucun horaire trouvé pour cet employé dans cette succursale.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de la récupération des horaires : {e}")

    def save_horaire(self):
        """Enregistrer les horaires modifiés dans la base de données."""
        # Collecter les horaires saisis
        horaires = {}
        jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]

        for i, jour in enumerate(jours):
            heure_entree = self.inputs[f'heure_entree_{jour}'].time().toString("HH:mm")
            heure_sortie = self.inputs[f'heure_sortie_{jour}'].time().toString("HH:mm")
            horaires[f'heure_entree_{jour}'] = heure_entree
            horaires[f'heure_sortie_{jour}'] = heure_sortie

        # Insérer ou mettre à jour les horaires dans la base de données
        try:
            db_manager = DatabaseManager('erp_database.db')
            query = """
                INSERT OR REPLACE INTO Horaires (id_employe, id_succursale, date,
                    heure_entree_lundi, heure_sortie_lundi,
                    heure_entree_mardi, heure_sortie_mardi,
                    heure_entree_mercredi, heure_sortie_mercredi,
                    heure_entree_jeudi, heure_sortie_jeudi,
                    heure_entree_vendredi, heure_sortie_vendredi, statut)
                VALUES (?, ?, date('now'),
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'actif')
            """

            values = (
                Emplacement.employeHoraire, Emplacement.succursalesId,
                horaires['heure_entree_lundi'], horaires['heure_sortie_lundi'],
                horaires['heure_entree_mardi'], horaires['heure_sortie_mardi'],
                horaires['heure_entree_mercredi'], horaires['heure_sortie_mercredi'],
                horaires['heure_entree_jeudi'], horaires['heure_sortie_jeudi'],
                horaires['heure_entree_vendredi'], horaires['heure_sortie_vendredi']
            )

            db_manager.execute_update(query, values)
            print("Les horaires ont été enregistrés avec succès.")

        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de l'enregistrement des horaires : {e}")
