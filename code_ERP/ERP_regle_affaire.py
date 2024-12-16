from datetime import datetime
from ERP_vue_dossier.rabais import *

def verify_regles(db_manager, client_id = None):
    rows = db_manager.execute_query("SELECT * FROM Regle_affaires",())
    all_rabais = []
    if not rows: return
    for regle in rows:
        
        id = regle[0]
        table = regle[1]      
        champ = regle[2]      
        operateur = regle[3]  
        valeur = regle[4]       #$
        action = regle[5]     
        message = regle[6]      #%
        date = regle[7] 
        statut = regle[8]
        date_debut = regle[9]
        date_fin = regle[10]
        
        print(f"{table} - {champ} - {valeur} - {action} - {message} - {statut} - {date}")   
        
        
        #switch de l'action
        if statut == "pending" or statut == "infinite":
            if action == "Envoyer email":

                if (statut == "pending" and date == datetime.now().strftime('%Y-%m-%d')) or (statut == "infinite" and date[5:] == datetime.now().strftime('%Y-%m-%d')[5:]): # si c'est la date d'aujourd'hui                
                    if valeur == "": # si la valeur est vide envoyer email a toute la table
                        result = db_manager.execute_query(f"SELECT email FROM {table}",())
                        for email in result:
                            envoyer_email(email[0], message)
                    else: 
                        result = db_manager.execute_query(f"SELECT email FROM {table} WHERE {champ} = '{valeur}'",())
                        if result:
                            envoyer_email(result[0][0], message)
                    
                    if statut == "pending":
                        db_manager.execute_query(f"Delete FROM Regle_affaires WHERE id_regle_affaire = '{id}'",())
                    elif statut == "infinite":  # pour dire bonne fete et ensuite lui dire d'attendre de ne plus etre la meme journé
                        db_manager.execute_update(f"UPDATE Regle_affaires SET statut = 'delayed' WHERE id_regle_affaire = {id}", ())
                        
                # si on plus la meme journée, réactiver la regle
                elif statut == "delayed" and date[5:] != datetime.now().strftime('%Y-%m-%d')[5:]:
                    db_manager.execute_update(f"UPDATE Regle_affaires SET statut = 'infinite' WHERE id_regle_affaire = {id}", ())
                    
            elif action == "Appliquer rabais":

                #Conversion des chaînes de caractères en objets datetime
                try:
                    date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
                    date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
                except:
                    db_manager.execute_query(f"Delete FROM Regle_affaires WHERE id_regle_affaire = '{id}'",())
                    return
                date_aujourdhui = datetime.today()

                # Vérifier si la date actuelle est entre date_debut et date_fin incluses
                if date_debut <= date_aujourdhui <= date_fin:
                    all_rabais.append(Rabais(message, operateur, valeur))
                elif date_aujourdhui > date_fin:
                    print("done", date_aujourdhui, date_fin)
                    db_manager.execute_query(f"Delete FROM Regle_affaires WHERE id_regle_affaire = '{id}'",())
                pass

    if action == "Appliquer rabais":
        return all_rabais

        
def envoyer_email(email, message):
    # envoyer message au email
    print(email, " -> ", message)