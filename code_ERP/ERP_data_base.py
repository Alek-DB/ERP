import sqlite3
from threading import Lock

class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, db_path='erp_database.db'):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON;")
        # créer les tables si elles n'existent pas
        self._create_tables()

    def _create_tables(self):
        
        # Création de la table Employes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employes (
            id_employe INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL,
            poste TEXT,
            salaire REAL,
            date_naissance TEXT,
            date_embauche TEXT,
            sexe TEXT CHECK(sexe IN ('M', 'F')),
            statut TEXT,
            allergies_preferences_alimentaires TEXT,
            mot_de_passe TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE
        )
        """)

        # Création de la table Roles 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            id_role INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_role TEXT NOT NULL,
            description TEXT
        )
        """)

        # Création de la table Employes_Roles 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employes_Roles (
            id_employe_role INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER NOT NULL,
            id_role INTEGER NOT NULL,
            date_debut TEXT,
            date_fin TEXT,
            FOREIGN KEY (id_employe) REFERENCES Employes(id_employe),
            FOREIGN KEY (id_role) REFERENCES Roles(id_role)
        )
        """)

        # Création de la table Succursales
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Succursales (
            id_succursale INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            gerant INTEGER,
            adresse TEXT,
            telephone TEXT,
            code TEXT,
            date_ouverture TEXT,
            statut TEXT,
            FOREIGN KEY (gerant) REFERENCES Employes(id_employe)
        )
        """)

        # Création de la table Employes_Succursales
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employes_Succursales (
            id_employe_succursale INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER NOT NULL,
            id_succursale INTEGER NOT NULL,
            date_debut TEXT,
            date_fin TEXT,
            FOREIGN KEY (id_employe) REFERENCES Employes(id_employe),
            FOREIGN KEY (id_succursale) REFERENCES Succursales(id_succursale)
        )
        """)

        # Création de la table Horaires
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Horaires (
            id_horaire INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER NOT NULL,
            id_succursale INTEGER NOT NULL,
            date TEXT,
            heure_entree_lundi TEXT,
            heure_sortie_lundi TEXT,
            heure_sortie_mardi TEXT,
            heure_entree_mardi TEXT,
            heure_sortie_mercredi TEXT,
            heure_entree_mercredi TEXT,
            heure_sortie_jeudi TEXT,
            heure_entree_jeudi TEXT,
            heure_sortie_vendredi TEXT,
            heure_entree_vendredi TEXT,
            
            statut TEXT,
            FOREIGN KEY (id_employe) REFERENCES Employes(id_employe),
            FOREIGN KEY (id_succursale) REFERENCES Succursales(id_succursale)
        )
        """)

        # Création de la table Clients
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            adresse TEXT,
            telephone TEXT,
            email TEXT,
            date_inscription TEXT,
            statut TEXT,
            notes TEXT
        )
        """)

        # Création de la table Fournisseurs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fournisseurs (
            id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT NOT NULL
        )

        """)

        # Création de la table Produits
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produits (
            id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            code_produit TEXT UNIQUE,
            nom_produit TEXT NOT NULL,
            prix REAL,
            description TEXT
        )
        """)
        
        #id_succursale INTEGER NOT NULL,
        #FOREIGN KEY (id_succursale) REFERENCES Succursales(id_succursale)

        # Création de la table Stocks
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stocks (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produit INTEGER NOT NULL,
            qte_actuelle INTEGER,
            qte_max INTEGER,
            qte_min_restock INTEGER,
            FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
        )
        """)

        # Création de la table Fournisseurs_Produits
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fournisseurs_Produits (
            id_fournisseur_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fournisseur INTEGER NOT NULL,
            id_produit INTEGER NOT NULL,
            prix_achat REAL,
            delai_livraison INTEGER,
            FOREIGN KEY (id_fournisseur) REFERENCES Fournisseurs(id_fournisseur),
            FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
        )
        """)

        # Création de la table Categories 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_categorie TEXT NOT NULL,
            description TEXT
        )
        """)

        # Création de la table Produits_Categories 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produits_Categories (
            id_produit_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produit INTEGER NOT NULL,
            id_categorie INTEGER NOT NULL,
            FOREIGN KEY (id_produit) REFERENCES Produits(id_produit),
            FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
        )
        """)

        # Création de la table Commandes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commandes (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fournisseur INTEGER,
            id_client INTEGER,
            date_commande TEXT,
            statut TEXT,
            total REAL,
            mode_paiement TEXT,
            date_livraison TEXT,
            adresse_livraison TEXT,
            notes TEXT,
            FOREIGN KEY (id_client) REFERENCES Clients(id_client)
        )
        """)

      # Création de la table Commandes_Produits
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commandes_Produits (
            id_commande_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER NOT NULL,
            id_produit INTEGER NOT NULL,
            quantite INTEGER,
            prix_unitaire REAL,
            total_ligne REAL,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande),
            FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
        )
        """)


        # Création de la table Achats
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Achats (
            id_achat INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fournisseur INTEGER,
            date_achat TEXT,
            statut TEXT,
            total REAL,
            notes TEXT,
            FOREIGN KEY (id_fournisseur) REFERENCES Fournisseurs(id_fournisseur)
        )
        """)

        # Création de la table Achats_Produits
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Achats_Produits (
            id_achat_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            id_achat INTEGER NOT NULL,
            id_produit INTEGER NOT NULL,
            quantite INTEGER,
            prix_unitaire REAL,
            total_ligne REAL,
            FOREIGN KEY (id_achat) REFERENCES Achats(id_achat),
            FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
        )
        """)

        # Création de la table Paiements 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paiements (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER,
            montant REAL,
            date_paiement TEXT,
            mode_paiement TEXT,
            statut TEXT,
            notes TEXT,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande)
        )
        """)

        # Création de la table Promotions 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Promotions (
            id_promotion INTEGER PRIMARY KEY AUTOINCREMENT,
            code_promo TEXT UNIQUE,
            description TEXT,
            pourcentage_remise REAL,
            date_debut TEXT,
            date_fin TEXT,
            statut TEXT
        )
        """)

        # Création de la table Commandes_Promotions 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commandes_Promotions (
            id_commande_promotion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER NOT NULL,
            id_promotion INTEGER NOT NULL,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande),
            FOREIGN KEY (id_promotion) REFERENCES Promotions(id_promotion)
        )
        """)

        # Création de la table Logistiques 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Logistiques (
            id_logistique INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER NOT NULL,
            statut_livraison TEXT,
            transporteur TEXT,
            numero_suivi TEXT,
            date_expedition TEXT,
            date_livraison TEXT,
            notes TEXT,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande)
        )
        """)

        # Création de la table Retours 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Retours (
            id_retour INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER NOT NULL,
            date_retour TEXT,
            motif TEXT,
            statut TEXT,
            notes TEXT,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande)
        )
        """)

        # Création de la table Comptabilite 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comptabilite (
            id_transaction INTEGER PRIMARY KEY AUTOINCREMENT,
            date_transaction TEXT,
            type_transaction TEXT,
            montant REAL,
            description TEXT,
            id_commande INTEGER,
            id_achat INTEGER,
            FOREIGN KEY (id_commande) REFERENCES Commandes(id_commande),
            FOREIGN KEY (id_achat) REFERENCES Achats(id_achat)
        )
        """)
        
        #création de la table Regle d'affaire
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Regle_affaires (
            id_regle_affaire INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            champ_name TEXT,
            operateur TEXT,
            valeur TEXT,
            action TEXT,
            desc TEXT
        )
        """)
        
        self._ensure_columns_exist('Fournisseurs', {
        'telephone': 'TEXT'
        })
        
        self._ensure_columns_exist('Commandes', {
        'id_fournisseur': 'INTEGER'
        })

        # Commit des changements
        self.connection.commit()

    def _ensure_columns_exist(self, table_name, columns):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        existing_columns = [col[1] for col in self.cursor.fetchall()]
        for column_name, column_type in columns.items():
            if column_name not in existing_columns:
                self.cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
                self.connection.commit()
    
    def execute_query(self, query, parameters=()):
        with self.connection:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()

    def execute_update(self, query, parameters=()):
        with self.connection:
            self.cursor.execute(query, parameters)
            self.connection.commit()
            return self.cursor.rowcount

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self._instance = None

    def __del__(self):
        self.close_connection()
        
    def get_column_names(self):
        """Retourne les noms des colonnes d'un curseur SQLite."""
        return [description[0] for description in self.cursor.description]
        
        
    def get_all_stocks(self):
        query = """
        SELECT Stocks.id_stock, Produits.nom_produit, Stocks.qte_actuelle, Stocks.qte_max, Stocks.qte_min_restock
        FROM Stocks
        JOIN Produits ON Stocks.id_produit = Produits.id_produit
        """
        return self.execute_query(query)




# Exemple d'Exécution d'une Requête SELECT
# python
# Copier le code
# try:
#     db_manager = DatabaseManager('erp_database.db')
#     query = "SELECT * FROM Employes WHERE id_employe = ?"
#     results = db_manager.execute_query(query, (1,))

#     for row in results:
#         nom = row['nom']
#         prenom = row['prenom']
#         print(f"Nom : {nom}, Prénom : {prenom}")

# except sqlite3.Error as e:
#     print(f"Une erreur est survenue : {e}")

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------    

# Exemple d'Exécution d'une Requête INSERT
# python
# Copier le code
# try:
#     db_manager = DatabaseManager('erp_database.db')
#     query = """
#     INSERT INTO Clients (nom, prenom, adresse, telephone, email, date_inscription, statut)
#     VALUES (?, ?, ?, ?, ?, date('now'), ?)
#     """
#     parameters = ("Dupont", "Jean", "123 Rue Principale", "0123456789", "jean.dupont@example.com", "Actif")
#     rows_affected = db_manager.execute_update(query, parameters)

#     if rows_affected > 0:
#         print("Le client a été ajouté avec succès.")

# except sqlite3.Error as e:
#     print(f"Une erreur est survenue : {e}")

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------    

# Exemple d'une Classe DAO pour les Employés
# python
# Copier le code
# class EmployeDAO:
#     def __init__(self, db_path='erp_database.db'):
#         self.db_manager = DatabaseManager(db_path)

#     def get_employe_by_id(self, id_employe):
#         query = "SELECT * FROM Employes WHERE id_employe = ?"
#         results = self.db_manager.execute_query(query, (id_employe,))
#         if results:
#             return results[0]  # Retourne le premier enregistrement trouvé
#         else:
#             return None

#     def add_employe(self, employe_data):
#         query = """
#         INSERT INTO Employes (nom, prenom, poste, salaire, date_naissance, date_embauche, sexe, statut, allergies_preferences_alimentaires, code_unique)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """
#         parameters = (
#             employe_data['nom'],
#             employe_data['prenom'],
#             employe_data['poste'],
#             employe_data['salaire'],
#             employe_data['date_naissance'],
#             employe_data['date_embauche'],
#             employe_data['sexe'],
#             employe_data['statut'],
#             employe_data['allergies_preferences_alimentaires'],
#             employe_data['code_unique']
#         )
#         rows_affected = self.db_manager.execute_update(query, parameters)
#         return rows_affected > 0

#     # Vous pouvez ajouter des méthodes pour mettre à jour et supprimer des employés
# Utilisation de EmployeDAO
# python
# 
# employe_dao = EmployeDAO()

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------    

# # Ajouter un employé
# employe_data = {
#     'nom': 'Martin',
#     'prenom': 'Sophie',
#     'poste': 'Comptable',
#     'salaire': 45000.00,
#     'date_naissance': '1985-06-15',
#     'date_embauche': '2022-01-10',
#     'sexe': 'F',
#     'statut': 'Actif',
#     'allergies_preferences_alimentaires': 'Aucune',
#     'code_unique': 'EMP202201'
# }

# if employe_dao.add_employe(employe_data):
#     print("L'employé a été ajouté avec succès.")

# # Récupérer un employé par ID
# employe = employe_dao.get_employe_by_id(1)
# if employe:
#     print(f"Nom : {employe['nom']}, Prénom : {employe['prenom']}")
# else:
#     print("Aucun employé trouvé avec cet ID.")