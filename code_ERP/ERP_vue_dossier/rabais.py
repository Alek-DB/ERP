class Rabais():
    def __init__(self, rabais, operateur, value) -> None:
        self.rabais = float(rabais)
        self.operateur = operateur
        self.value = float(value)
        self.title = f"Vous avez un rabais de {self.rabais}% pour un total de commande {self.operateur} {self.value}$"
        
        
operateurs = {
    "<": "lt",
    "<=": "le",
    ">": "gt",
    ">=": "ge",
    "=": "eq",
    "!=": "ne"
}