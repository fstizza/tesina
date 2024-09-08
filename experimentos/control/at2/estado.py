from json import dump, loads
from os.path import exists


class Estado:
    """Modelo que representa el estado del sistema."""

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        # TODO: Mapear propiedades del Estado al JSON
        json["Accs"] = self.accs
        json["AdmAcc"] = self.admacc
        json["Money"] = self.money
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
            # TODO: Mapear propiedades del objeto JSON a la instancia del estado.
            estado.accs = json["Accs"]
            estado.admacc = json["AdmAcc"]
            estado.money = json["Money"]
            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        # TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
        estado.accs = [{
            "DNI": 39213546,
            "Clave": "70065",
            "NyA": "Roberto Colectivos",
            "Saldo": 300000,
            "Hist": []
        }, {
            "DNI": 22334980,
            "Clave": "66666",
            "NyA": "Aquiles Bailoyo",
            "Saldo": 20,
            "Hist": []
        }]
        estado.admacc = [{"Clave": "12345", "DNI": 107, "Movs": []}]
        estado.money = 70000000000
        return estado


Estado.cargar = staticmethod(Estado.cargar)
""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
