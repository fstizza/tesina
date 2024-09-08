from json import dump, loads
from os.path import exists


class Estado:
    """Modelo que representa el estado del sistema."""


    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["admins"] = self.admins
        json["usuarios"] = self.usuarios
        json["logs"]=self.logs
        json["cuentas"]=self.cuentas
        json["disponible"]=self.disponible
        json["totalUsers"]=self.totalusers
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
            estado.admins = json["admins"]
            estado.usuarios = json["usuarios"]
            estado.logs = json["logs"]
            estado.cuentas = json["cuentas"]
            estado.disponible = json["disponible"]
            estado.totalusers = json["totalUsers"]
            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        estado.admins = {}
        estado.usuarios = {}
        estado.logs = {}
        estado.cuentas = {}
        estado.disponible = 0
        estado.totalusers = 0

        return estado


Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
