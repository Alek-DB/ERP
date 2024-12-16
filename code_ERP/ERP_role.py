class Role:
    ROLE_ADMINISTRATEUR = 1
    ROLE_GERANT_GLOBAL = 2
    ROLE_GERANT = 3
    ROLE_HR = 4
    ROLE_COMMIS = 5
    ROLE_FINANCE = 6

    @staticmethod
    def get_role_name(role):
        return roles.get(role, "Inconnu")

roles = {
    Role.ROLE_ADMINISTRATEUR: "Administrateur",
    Role.ROLE_GERANT_GLOBAL: "Gérant Global",
    Role.ROLE_GERANT: "Gérant (Magasin)",    
    Role.ROLE_HR: "HR",
    Role.ROLE_COMMIS: "Commis",
    Role.ROLE_FINANCE: "Finance",
}