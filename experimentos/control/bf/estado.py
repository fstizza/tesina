from json import dump, loads
from os.path import exists


class Estado:
    """Modelo que representa el estado del sistema."""

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        # TODO: Mapear propiedades del Estado al JSON
        # json["propiedad1"] = self.propiedad1;
        json["usuarios"] = self.usuarios
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
            if ["usuarios", "saldo"] == list(json.keys()):
                estado = Estado()
                # TODO: Mapear propiedades del objeto JSON a la instancia del estado.
                # estado.propiedad1 = json["propiedad1"]
                estado.usuarios = json["usuarios"]
                estado.saldo = json["saldo"]
                return estado
        
        return Estado.__inicial()
        

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        # TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
        # estado.propiedad1 = valor;
        estado.usuarios = { "-1" : {
                                    "nombre": "admin",
                                    "apellido": "admin",
                                    "sueldo": 0,
                                    "clave": "admin",
                                    "saldo": 0,
                                    "movimientos": {},
                                    "admin": True
                                }
                        }  
        estado.saldo = 0
        return estado


Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
