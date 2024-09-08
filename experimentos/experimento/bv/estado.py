from json import dump, loads
from os.path import exists
from movs import movs_to_str,movs_from_str

class Estado:
    """Modelo que representa el estado del sistema."""
    CANT_MAX_USUARIOS = 5
    LONG_MIN_CLAVE = 8
    DNI_ADMIN = "41456789"
    NOMBRE_ADMIN = "Federico Stizza"
    CLAVE_ADMIN = "clavefede"

    def __init__ (self):
        self.usuarios = {}
        self.claves = {}
        self.saldos = {}
        self.sueldos = {}
        self.movimientos = {}
        self.saldo = 0

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["usuarios"] = self.usuarios
        json["claves"] = self.claves
        json["saldos"] = self.saldos
        json["sueldos"] = self.sueldos
        json["movimientos"] = movs_to_str(self.movimientos)
        json["saldo"] = self.saldo
        with open("estado.json", "w") as estado_archivo:
            dump(json, estado_archivo)

    def cargar():
        """Retorna una instancia del modelo de estado con los valores guardados en `estado.json`."""
        contenido = ""
        if exists("estado.json"):
            with open("estado.json", "r") as estado_archivo:
                contenido = estado_archivo.read()
        if contenido != "":
            json = loads(contenido)
            estado = Estado()
            estado.usuarios = json["usuarios"]
            estado.claves = json["claves"]
            estado.saldos = json["saldos"]
            estado.sueldos = json["sueldos"]
            estado.movimientos = movs_from_str(json["movimientos"])
            estado.saldo = json["saldo"]
            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        estado.usuarios[estado.DNI_ADMIN] = estado.NOMBRE_ADMIN
        estado.claves[estado.DNI_ADMIN] = estado.CLAVE_ADMIN
        return estado


Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
