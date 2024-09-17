from tipos import DNI, CLAVE, MONTO, NOMBRE


class Usuario:
    saldo: MONTO
    sueldo: MONTO
    clave: CLAVE
    nombre: NOMBRE
    dni: DNI

    def __init__(self, json=None):
        if json != None:
            self.saldo = int(json["saldo"])
            self.sueldo = int(json["sueldo"])
            self.clave = json["clave"]
            self.nombre = json["nombre"]
            self.dni = json["dni"]

    def aJson(self):
        return {
            "saldo": self.saldo,
            "sueldo": self.sueldo,
            "clave": self.clave,
            "nombre": self.nombre,
            "dni": self.dni,
        }
