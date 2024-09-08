from abst_types import DNI, CLAVE, NOMBRE, FECHAHORA
from syn_types import MONTO
from enums import OPERACION

import re
from datetime import datetime
from json import dump, loads
from os.path import exists


def str_to_datetime(date):
    arg_list = map(lambda n: int(n), re.split(r',|\:| |\-|\.', date))

    return datetime(*arg_list)

class Estado:
    """Modelo que representa el estado del sistema."""
    CANT_MAX_USUARIOS : int = 5
    LONG_MIN_CLAVE : int = 8
    ADMINISTRADOR : DNI = "40278173"
    NOMBRE_ADMINISTRADOR : NOMBRE = "admin_nombre"
    CLAVE_ADMINISTRADOR : CLAVE = "0123456789"
    AHORA : FECHAHORA = FECHAHORA.now() #esta mal que esto pertenzca a la clase, deberia ir al main creo

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["usuarios"] = self.usuarios
        json["claves"] = self.claves
        json["saldos"] = self.saldos
        json["sueldos"] = self.sueldos
        json["movimientos"] = {k: list(v) for k, v in self.movimientos.items()}
        json["saldo"] = self.saldo

        with open("estado.json", "w") as estado_archivo:
            dump(json, estado_archivo, indent=2, sort_keys=True, default=str)

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

            estado.movimientos = {k: set([(str_to_datetime(m[0]), m[1]) for m in movs]) for k, movs in json["movimientos"].items()}
            estado.saldo = json["saldo"]

            return estado
        else:
            return Estado.__inicial()

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        estado.usuarios = {estado.ADMINISTRADOR: estado.NOMBRE_ADMINISTRADOR}
        estado.claves = {estado.ADMINISTRADOR: estado.CLAVE_ADMINISTRADOR}
        estado.saldos = {}
        estado.sueldos = {}
        estado.movimientos = {}
        estado.saldo = 0
        return estado

    usuarios : dict[DNI, NOMBRE]
    claves : dict[DNI, CLAVE]
    saldos : dict[DNI, MONTO]
    sueldos : dict[DNI, MONTO]
    movimientos : dict[DNI, set[FECHAHORA, OPERACION]]
    saldo: MONTO



Estado.cargar = staticmethod(Estado.cargar)

""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
