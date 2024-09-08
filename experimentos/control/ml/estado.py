from json import dump, loads
from os.path import exists
from entidades.cajero import Cajero
from entidades.usuario import Cuenta, Usuario

class Estado:
    """Modelo que representa el estado del sistema."""

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {} 
        json["usuarios"] = [usuario.to_dict() for usuario in self.usuarios]
        json["cajero"] = self.cajero.to_dict()

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
            estado.usuarios = [Usuario.from_json(usuario_json) for usuario_json in json["usuarios"]]
            estado.cajero = Cajero.from_json(json["cajero"])

            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        cuenta = Cuenta(0,[])
        admin = Usuario(391238934,"clave","admin",0,True,cuenta)

        estado.usuarios = [admin]
        estado.cajero = Cajero(0)

        return estado


Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
