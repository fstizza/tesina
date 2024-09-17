from tipos import FECHAHORA, DNI, OPERACION
from constantes import FORMATO_FECHA
from datetime import datetime


class Movimiento:
    fechahora: FECHAHORA
    operacion: OPERACION
    dni: DNI

    def __init__(self, fechahora: datetime, operacion: OPERACION, dni: DNI):
        self.fechahora = fechahora
        self.operacion = operacion
        self.dni = dni

    @classmethod
    def desde_json(self, json=None):
        if json != None:
            fechahora = datetime.strptime(json["fecha"], FORMATO_FECHA)
            operacion = OPERACION(json["op"])
            dni = json["dni"]
            return Movimiento(fechahora, operacion, dni)

    def aJson(self):
        return {
            "fecha": self.fechahora.strftime(FORMATO_FECHA),
            "op": int(self.operacion),
            "dni": self.dni,
        }
