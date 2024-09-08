import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%S.%fZ"


def mapearUsuario(datos: map) -> Usuario:
    dni = datos["dni"]
    nombre = datos["nombre"]
    clave = datos["clave"]
    sueldo = int(datos["sueldo"])
    saldo = int(datos["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: map):
    fecha = datetime.strptime(datos["fecha"], FORMATO_FECHA)
    dni = datos["dni"]
    operacion = ""
    valor = -1
    if datos["tipo"] == "extraccion":
        operacion = 1
        valor = int(datos["monto"])
    elif datos["tipo"] == "clave":
        operacion = 2
    return Movimiento(dni, operacion, fecha, valor)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "clave"
    return res


def movimientoToJson(movimiento: Movimiento) -> map:
    res = {
        "tipo": mapearIdOperacionStr(movimiento.operacion),
        "dni": movimiento.dni,
        "fecha": movimiento.fecha.strftime(FORMATO_FECHA),
    }

    if movimiento.operacion == 1:
        res["monto"] = movimiento.valor if movimiento.valor is not None else 0

    return res


class AdaptadorPG(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = list(
                map(mapearUsuario, estado_json["usuarios"]),
            )

            movimientos = list(
                map(mapearMovimiento, estado_json["movimientos"]),
            )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["cajero"]["saldo"])
            return estado

    def guardar(self, estado: Estado):
        cajero = {"saldo": estado.saldo}
        usuarios = list(
            map(
                lambda u: {
                    "dni": u.dni,
                    "nombre": u.nombre,
                    "clave": u.clave,
                    "sueldo": u.sueldo,
                    "saldo": u.saldo,
                    "admin": u.nombre == "admin",
                },
                estado.usuarios,
            )
        )
        movimientos = list(
            map(movimientoToJson, estado.movimientos),
        )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "movimientos": movimientos,
                    "cajero": cajero,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "0"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%Y-%m-%d")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]
            return list(map(movimientoDesdeStdout, lineas))
        except:
            return []


def movimientoDesdeStdout(linea: str) -> Movimiento:
    if "extraccion" in linea:
        fecha, _, monto = linea.split(" - ")
        fecha = datetime.strptime(fecha.strip(), FORMATO_FECHA)
        monto = int(monto.strip()[1:])
        return Movimiento("-1", 1, fecha, monto)
    elif "clave" in linea:
        fecha, _ = linea.split(" - ")
        fecha = datetime.strptime(fecha.strip(), FORMATO_FECHA)
        return Movimiento("-1", 2, fecha)


"""
EJEMPLO ESTADO
{
    "usuarios": [
        {
            "dni": "0",
            "nombre": "admin",
            "clave": "admin",
            "sueldo": 0,
            "saldo": 0,
            "admin": true
        },
        {
            "dni": "41404842",
            "nombre": "federico",
            "clave": "Prueba321",
            "sueldo": 10000,
            "saldo": 9000,
            "admin": false
        }
    ],
    "cajero": {
        "saldo": 9000
    },
    "movimientos": [
        {
            "tipo": "extraccion",
            "dni": "41404842",
            "fecha": "2023-11-07T00:20:56.479Z",
            "monto": 1000
        },
        {
            "tipo": "clave",
            "dni": "41404842",
            "fecha": "2023-11-07T00:21:10.414Z"
        }
    ]
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Movimientos de federico:
2023-11-07T00:20:56.479Z - extraccion - $1000
2023-11-07T00:21:10.414Z - clave
"""
