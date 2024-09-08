class Cajero:
    def __init__(self,monto):
        self.monto = monto 

    def extraer(self, monto):
        if monto > self.monto:
            return "Saldo insuficiente en el cajero" 

        self.monto  -= monto 

    def cargar(self, monto):
        self.monto  += monto 

    def to_dict(self):
        return { 
            "monto": self.monto 
        }

    @classmethod
    def from_json(cls,data):
        return cls(
            data["monto"]
        )



