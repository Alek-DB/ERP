from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt
from utils.QListe import QListe  # Importez la classe QListe


class HR_Commandes(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Main layout for Employee interface
        main_layout = QVBoxLayout()

        # Création de la barre de recherche
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher une commande")
        search_button = QPushButton("Rechercher")
        search_button.clicked.connect(self.rechercher_commande)
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)
        
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(back_button)
        search_layout.addWidget(search_button)

        
        # Création de la liste des commandes
        self.commande_liste = QListe("Commandes", [], ["Numéro", "Date", "Client"])

        main_layout.addWidget(self.commande_liste)
        main_layout.addLayout(search_layout)


        self.setLayout(main_layout)

    def rechercher_commande(self):
        # Récupération du numéro de commande saisi
        numero_commande = self.search_bar.text()

        # Requête pour récupérer les informations de la commande
        # (remplacez par votre requête SQL ou votre méthode de récupération de données)
        commande = self.get_commande_from_db(numero_commande)

        if commande:
            # Création de la liste des objets pour la classe QListe
            objects = [
                [commande["numero"], commande["date"], commande["client"]]
            ]

            # Mise à jour de la liste des commandes
            self.commande_liste = QListe("Commandes", objects, ["Numéro", "Date", "Client"])
            self.layout().addWidget(self.commande_liste)
        else:
            print("Commande non trouvée")

    def get_commande_from_db(self, numero_commande):
        # Requête pour récupérer les informations de la commande depuis la base de données
        # (remplacez par votre requête SQL ou votre méthode de récupération de données)
        query = "SELECT * FROM commandes WHERE numero = ?"
        # Exécution de la requête et récupération des résultats
        # (remplacez par votre méthode d'exécution de requête et de récupération de résultats)
        result = {"numero": numero_commande, "date": "2022-01-01", "client": "Client 1"}
        return result