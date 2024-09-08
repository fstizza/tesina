from json import dump, loads
from os.path import exists


class Estado:
    """Modelo que representa el estado del sistema."""

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["admin_user"] = self.admin_user
        json["admin_pass"] = self.admin_pass
        json["user_list"] = self.user_list
        json["account_list"] = self.account_list
        json["mov_list"] = self.mov_list
        json["saldo_cajero"] = self.saldo_cajero
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
            estado.admin_user = json["admin_user"]
            estado.admin_pass = json["admin_pass"]
            estado.user_list = json["user_list"]
            estado.account_list = json["account_list"]
            estado.mov_list = json["mov_list"]
            estado.saldo_cajero = json["saldo_cajero"]
            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        estado.admin_user = "admin"
        estado.admin_pass = "pass_admin"
        estado.user_list = []
        estado.account_list = []
        estado.mov_list = (
            []
        )  # {"mov_type": "extraccion", "dni": "39950090", "saldo": 1, "date": fecha}
        estado.saldo_cajero = 0
        return estado


Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
