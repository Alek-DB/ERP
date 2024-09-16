import tkinter as tk
from tkinter import messagebox
import requests


# Classe Modèle
class Modele:
    def __init__(self):
        self.authenticated = False

    def verifier_identifiants(self, username, password):
        # Simule une requête au serveur pour vérifier les identifiants
        try:
            response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200 and response.json().get('success'):
                self.authenticated = True
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return False

    def creer_vente(self, item, quantite, prix_unitaire, date):
        # Simule une requête pour créer une vente
        vente_data = {
            'item': item,
            'quantite': quantite,
            'prix_unitaire': prix_unitaire,
            'date': date
        }
        try:
            response = requests.post('http://localhost:5000/vente', json=vente_data)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return False


# Classe Vue
class Vue:
    def __init__(self, controleur):
        self.controleur = controleur
        self.root = tk.Tk()
        self.root.title("Application ERP")

        # Initialisation des frames
        self.frame_connexion = None
        self.frame_vente = None
        self.frame_splash = None

        # Construction des frames
        self.construire_frame_connexion()
        self.construire_frame_vente()
        self.construire_frame_splash()

        # Affichage initial
        self.basculer_vers_connexion()

    def centrer_fenetre(self):
        # Mettre à jour la géométrie de la fenêtre
        self.root.update_idletasks()

        # Obtenir la taille de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtenir la taille de la fenêtre
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Calculer la position pour centrer la fenêtre
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Définir la géométrie de la fenêtre
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def construire_frame_connexion(self):
        self.frame_connexion = tk.Frame(self.root, width=300, height=200)
        self.frame_connexion.pack_propagate(False)

        # Frame pour le titre
        frame_titre = tk.Frame(self.frame_connexion)
        frame_titre.pack(pady=(20, 10))

        label_titre = tk.Label(frame_titre, text="Connexion ERP", font=("Helvetica", 16, "bold"))
        label_titre.pack()

        # Frame pour les champs de connexion
        frame_champs = tk.Frame(self.frame_connexion)
        frame_champs.pack(pady=10)

        self.label_username = tk.Label(frame_champs, text="Nom d'utilisateur")
        self.entry_username = tk.Entry(frame_champs)
        self.label_password = tk.Label(frame_champs, text="Mot de passe")
        self.entry_password = tk.Entry(frame_champs, show="*")

        self.label_username.grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.entry_username.grid(row=0, column=1, padx=5, pady=2)
        self.label_password.grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.entry_password.grid(row=1, column=1, padx=5, pady=2)

        # Frame pour le bouton de connexion
        frame_bouton = tk.Frame(self.frame_connexion)
        frame_bouton.pack(pady=10)

        self.button_login = tk.Button(frame_bouton, text="Se connecter", command=self.controleur.se_connecter)
        self.button_login.pack()


    def construire_frame_vente(self):
        self.frame_vente = tk.Frame(self.root, width=600, height=400)
        self.frame_vente.pack_propagate(False)

        # Frame pour le titre et l'explication
        frame_titre = tk.Frame(self.frame_vente)
        frame_titre.pack(pady=(20, 10), fill='x')

        self.label_titre_vente = tk.Label(frame_titre, text="Enregistrement des ventes", font=("Helvetica", 18, "bold"))
        self.label_titre_vente.pack()

        self.label_explication = tk.Label(frame_titre, text="Veuillez remplir les champs ci-dessous pour enregistrer une nouvelle vente.", font=("Helvetica", 10), wraplength=500)
        self.label_explication.pack(pady=(5, 0))

        # Frame pour les champs d'entrée
        frame_entrees = tk.Frame(self.frame_vente)
        frame_entrees.pack(pady=10)

        self.label_item = tk.Label(frame_entrees, text="Article", font=("Helvetica", 12))
        self.entry_item = tk.Entry(frame_entrees, font=("Helvetica", 12))
        self.label_quantite = tk.Label(frame_entrees, text="Quantité", font=("Helvetica", 12))
        self.entry_quantite = tk.Entry(frame_entrees, font=("Helvetica", 12))
        self.label_prix = tk.Label(frame_entrees, text="Prix Unitaire", font=("Helvetica", 12))
        self.entry_prix = tk.Entry(frame_entrees, font=("Helvetica", 12))
        self.label_date = tk.Label(frame_entrees, text="Date", font=("Helvetica", 12))
        self.entry_date = tk.Entry(frame_entrees, font=("Helvetica", 12))

        self.label_item.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_item.grid(row=0, column=1, padx=10, pady=5)
        self.label_quantite.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_quantite.grid(row=1, column=1, padx=10, pady=5)
        self.label_prix.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_prix.grid(row=2, column=1, padx=10, pady=5)
        self.label_date.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.entry_date.grid(row=3, column=1, padx=10, pady=5)

        # Frame pour les boutons
        frame_boutons = tk.Frame(self.frame_vente)
        frame_boutons.pack(pady=20)

        self.button_enregistrer_vente = tk.Button(frame_boutons, text="Accepter vente", command=self.controleur.enregistrer_vente, font=("Helvetica", 12))
        self.button_enregistrer_vente.pack(side=tk.LEFT, padx=10)

        self.button_annuler = tk.Button(frame_boutons, text="Annuler", command=self.controleur.annuler_vente, font=("Helvetica", 12))
        self.button_annuler.pack(side=tk.LEFT, padx=10)

    def construire_frame_splash(self):
        self.frame_splash = tk.Frame(self.root, width=600, height=400)
        self.frame_splash.pack_propagate(False)

        self.label_title = tk.Label(self.frame_splash, text="ERP Manager", font=("Helvetica", 24, "bold"))
        self.label_subtitle = tk.Label(self.frame_splash, text="Système de gestion intégré pour votre entreprise",
                                       font=("Helvetica", 12))

        self.button_frame = tk.Frame(self.frame_splash)
        self.button_gestion = tk.Button(self.button_frame, text="Gestion interne",
                                        command=lambda: self.controleur.action_splash("gestion"))
        self.button_options = tk.Button(self.button_frame, text="Options d'utilisation",
                                        command=lambda: self.controleur.action_splash("options"))
        self.button_formulaire = tk.Button(self.button_frame, text="Formulaire",
                                           command=lambda: self.controleur.action_splash("formulaire"))

        self.label_title.pack(pady=(50, 10))
        self.label_subtitle.pack(pady=(0, 50))
        self.button_frame.pack()
        self.button_gestion.pack(side=tk.LEFT, padx=10)
        self.button_options.pack(side=tk.LEFT, padx=10)
        self.button_formulaire.pack(side=tk.LEFT, padx=10)

    def afficher_message(self, titre, message):
        messagebox.showinfo(titre, message)

    def basculer_vers_connexion(self):
        self.frame_vente.pack_forget() if hasattr(self, 'frame_vente') else None
        self.frame_splash.pack_forget() if hasattr(self, 'frame_splash') else None
        self.frame_connexion.pack()
        self.centrer_fenetre()

    def basculer_vers_splash(self):
        self.frame_connexion.pack_forget()
        self.frame_vente.pack_forget()
        self.frame_splash.pack()

        self.root.geometry('600x400')
        self.centrer_fenetre()

    def basculer_vers_vente(self):
        self.frame_splash.pack_forget()
        self.frame_vente.pack()

        self.root.geometry('600x400')
        self.centrer_fenetre()

    def obtenir_identifiants(self):
        return self.entry_username.get(), self.entry_password.get()

    def obtenir_informations_vente(self):
        item = self.entry_item.get()
        quantite = self.entry_quantite.get()
        prix_unitaire = self.entry_prix.get()
        date = self.entry_date.get()
        return item, quantite, prix_unitaire, date

    def demarrer(self):
        self.root.mainloop()


# Classe Contrôleur modifiée
class Controleur:
    def __init__(self):
        self.modele = Modele()
        self.vue = Vue(self)

    def se_connecter(self):
        username, password = self.vue.obtenir_identifiants()
        if self.modele.verifier_identifiants(username, password):
            self.vue.afficher_message("Succès", "Connexion réussie !")
            self.vue.basculer_vers_splash()
        else:
            self.vue.afficher_message("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def action_splash(self, action):
        if action == "gestion":
            self.vue.afficher_message("Gestion interne", "Fonctionnalité non implémentée")
        elif action == "options":
            self.vue.afficher_message("Options d'utilisation", "Fonctionnalité non implémentée")
        elif action == "formulaire":
            self.vue.basculer_vers_vente()

    def enregistrer_vente(self):
        item, quantite, prix_unitaire, date = self.vue.obtenir_informations_vente()
        if self.modele.creer_vente(item, quantite, prix_unitaire, date):
            self.vue.afficher_message("Succès", "Vente enregistrée avec succès.")
        else:
            self.vue.afficher_message("Erreur", "Erreur lors de l'enregistrement de la vente.")

    def annuler_vente(self):
        # Retourner au splash screen
        self.vue.basculer_vers_splash()

    def demarrer(self):
        self.vue.demarrer()


# Démarrage de l'application
if __name__ == "__main__":
    app = Controleur()
    app.demarrer()
