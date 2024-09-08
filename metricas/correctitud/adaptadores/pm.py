import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime


def mapearUsuario(datos: map, estado: map, admin: bool = False) -> Usuario:
    clave = ""
    nombre = ""
    if admin:
        nombre = "__admin"
    sueldo = -1
    saldo = -1
    dni = ""

    claves = datos.keys()
    if "dni" in claves:
        dni = str(datos["dni"])
    if "clave" in claves:
        clave = str(datos["clave"])
    if "nombre" in claves:
        nombre = str(datos["nombre"])
    if "sueldo_mensual" in claves:
        sueldo = int(datos["sueldo_mensual"])

    cuentas_dni = list(
        filter(
            lambda c: str(c["dni"]) == dni,
            estado["cuentas"]
        )
    )

    saldo = -1
    if len(cuentas_dni) != 0:
        saldo = int(cuentas_dni[0]["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: map):
    # No persiste fecha de operacion
    dni = datos["dni"]
    operacion = datos["tipo"]

    idOp = -1
    if (operacion == "Extraccion"):
        idOp = 1
    elif (operacion == "Cambio password"):
        idOp = 2
    return Movimiento(dni, idOp, datetime.min)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'Extraccion'
    elif (id == 2):
        res = "Cambio password"
    return res


class AdaptadorPM(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = list(
                map(
                    lambda u: mapearUsuario(u, estado_json),
                    estado_json["usuarios"]

                )
            )

            usuarios_adm = list(
                map(
                    lambda u: mapearUsuario(u, estado_json, admin=True),
                    estado_json["admins"],

                )
            )

            usuarios = usuarios + usuarios_adm

            movimientos = list(
                map(
                    lambda m: mapearMovimiento(m),
                    estado_json["logs"]
                )
            )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["disponible"])
            return estado

    def guardar(self, estado: Estado):

        usuarios = filter(lambda u: u.nombre != '__admin', estado.usuarios)

        usuarios = list(
            map(
                lambda u: {
                    "dni": int(u.dni),
                    "clave": u.clave,
                    "nombre": u.nombre,
                    "sueldo_mensual": u.sueldo
                },
                usuarios
            )
        )

        admins = list(filter(lambda u: u.nombre == '__admin', estado.usuarios))

        admins = list(
            map(
                lambda u: {
                    "dni": int(u.dni),
                    "clave": u.clave,
                    "nombre": u.nombre,
                    "sueldo_mensual": u.sueldo
                },
                admins
            )
        )

        cuentas = list(
            map(
                lambda u: {
                    "dni": int(u.dni),
                    "saldo": u.saldo
                },
                estado.usuarios
            )
        )

        logs = list(
            map(
                lambda m: {
                    "dni": m.dni,
                    "tipo": mapearIdOperacionStr(m.operacion),
                    "valor": 0
                },
                estado.movimientos
            )
        )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "admins": admins,
                    "logs": logs,
                    "cuentas": cuentas,
                    "disponible": estado.saldo,
                    "totalUsers": len(usuarios),
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "40278173"
        NOMBRE_ADMIN = "__admin"
        CLAVE_ADMIN = "0123456789"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        """ No utiliza fecha en movimientos """
        return ""

    def movimientoDesdeString(self, datos: str):
        _, dni, operacion, valor = datos.split()

        idOp = -1
        if (operacion == "Extraccion"):
            idOp = 1
        elif (operacion == "Cambio password"):
            idOp = 2

        return Movimiento(dni, idOp, datetime.now(), valor)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            return list(map(self.movimientoDesdeString, salida.split('\n')[3:]))
        except:
            return []


"""
EJEMPLO ESTADO

{
    "admins": [
        {
            "dni": 40278173,
            "clave": "0123456789",
            "nombre": "__admin",
            "sueldo_mensual": 0
        }
    ],
    "usuarios": [
        {
            "dni": 41404842,
            "clave": "123456789",
            "nombre": "fede",
            "sueldo_mensual": 10000
        }
    ],
    "logs": [
        {
            "dni": 41404842,
            "tipo": "Extraccion",
            "valor": 100
        }
    ],
    "cuentas": [
        {
            "dni": 40278173,
            "saldo": 0
        },
        {
            "dni": 41404842,
            "saldo": 9900
        }
    ],
    "disponible": 19900,
    "totalUsers": 2
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Movimientos del cajero:
_______________________

Usuario:  41404842   Extraccion   100
"""