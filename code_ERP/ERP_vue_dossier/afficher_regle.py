from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from ERP_emplacement import Emplacement
from ERP_data_base import DatabaseManager


class QAfficheRegle(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.db_manager = DatabaseManager('erp_database.db')
        
        layout = QVBoxLayout()
        
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        
        layout.addWidget(back_button, alignment=Qt.AlignLeft)
        
        titre = QLabel("Règles")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titre)

        self.regle_layout = QVBoxLayout()
        
        layout.addLayout(self.regle_layout)
        self.setLayout(layout)
        
        self.load_data()  # Charge les données au départ
        
    def load_data(self):
        # Vider le layout avant de recharger les données
        for i in reversed(range(self.regle_layout.count())):
            widget = self.regle_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Supprimer les widgets précédemment ajoutés

        # Recharger les données depuis la base de données
        rows = self.db_manager.execute_query("SELECT * FROM Regle_affaires", ())
        for regle in rows:
            id = regle[0]
            table = regle[1]
            champ = regle[2]
            operateur = regle[3]
            valeur = regle[4]  # $
            action = regle[5]
            message = regle[6]  # %
            date = regle[7]
            statut = regle[8]
            date_debut = regle[9]
            date_fin = regle[10]

            line = QHBoxLayout()
            line.addWidget(QLabel(f"{id} - {action} - {table} - {champ} - {valeur} - {operateur} - {message} - {date} - {date_debut} - {date_fin} - {statut}"))
            
            # Créer le bouton de suppression
            btn = QPushButton("delete")
            btn.clicked.connect(lambda _, id=id: self.delete_regle(id))  # Appel de la méthode de suppression
            btn.setFixedWidth(100)
            line.addWidget(btn)
            self.regle_layout.addLayout(line)  # Ajouter la ligne au layout

    def delete_regle(self, id):
        # Exécuter la requête de suppression
        self.db_manager.execute_query(f"DELETE FROM Regle_affaires WHERE id_regle_affaire = '{id}'", ())
        
        # Recharger les données après la suppression
        self.load_data()
