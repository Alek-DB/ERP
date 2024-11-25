
def verify_regles(db_manager):
    rows = db_manager.execute_query("SELECT * FROM Regle_affaires",())
    print(rows)
    for regle in rows:
        table = regle[1]      
        champ = regle[2]      
        operateur = regle[3]  
        valeur = regle[4]     
        action = regle[5]     
        message = regle[6]    
        
        print(table)
        print(champ)
        print(operateur)
        print(valeur)
        print(action)
        print(message)
        
        #switch de l'action
        if action == "Envoyer email":
            pass
        elif action == "Appliquer rabais":
            pass
        
        
        # query = f"SELECT {champ} FROM {table} WHERE {champ} = ?"
        # employee_data = db_manager.execute_query(query, (valeur,))