class Role:
    ROLE_ADMINISTRATEUR = 1
    ROLE_HR = 2
    ROLE_GERANT = 3
    ROLE_COMMIS = 4

    @staticmethod
    def get_role_name(role):
        roles = {
            Role.ROLE_ADMINISTRATEUR: "Administrateur",
            Role.ROLE_HR: "HR",
            Role.ROLE_GERANT: "Gérant (Magasin)",
            Role.ROLE_COMMIS: "Commis"
        }
        return roles.get(role, "Inconnu")
