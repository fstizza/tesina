import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, "%Y-%m-%dT%H:%M:%S.%f0-03:00")


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["claves"].keys():
        clave = estado["claves"][dni]
    if dni in estado["usuarios"].keys():
        nombre = estado["usuarios"][dni]
    if dni in estado["sueldos"].keys():
        sueldo = int(estado["sueldos"][dni])
    if dni in estado["saldos"].keys():
        saldo = int(estado["saldos"][dni])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: list):
    fecha, operacion = datos
    fecha = parser.parse(fecha)
    idOp = -1
    if operacion == 0:
        idOp = 1
    elif operacion == 1:
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def mapearIdOperacionInt(id: int) -> int:
    res = -1
    if id == 1:
        res = 0
    elif id == 2:
        res = 1
    return res


class AdaptadorGT(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(map(lambda dni: mapearUsuario(estado_json, dni), dnis))

            movimientos = []

            for dni in dnis:
                if dni in estado_json["movimientos"].keys():
                    movimientos_dni = estado_json["movimientos"][dni].items()
                    movimientos.extend(
                        list(map(lambda m: mapearMovimiento(dni, m), movimientos_dni))
                    )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}
        claves = {}
        saldos = {}
        sueldos = {}
        movimientos = {}

        for usuario in estado.usuarios:
            usuarios[usuario.dni] = usuario.nombre
            claves[usuario.dni] = usuario.clave
            saldos[usuario.dni] = usuario.saldo
            sueldos[usuario.dni] = usuario.sueldo
            movimientos_usuario = filter(
                lambda m: m.dni == usuario.dni, estado.movimientos
            )
            movimientos_usuario = {
                formatearFecha(m.fecha): mapearIdOperacionInt(m.operacion)
                for m in movimientos_usuario
            }

            movimientos[usuario.dni] = movimientos_usuario

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "claves": claves,
                    "saldos": saldos,
                    "sueldos": sueldos,
                    "movimientos": movimientos,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "12345678"
        NOMBRE_ADMIN = "admin_nombre"
        CLAVE_ADMIN = "admin123"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%Y-%m-%dT%H:%M:%S")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]
            lineas = list(
                filter(lambda x: x != "", list(map(lambda l: l.strip(), lineas)))
            )
            movs = list(
                map(
                    lambda l: movimientoDesdeStdout(l.split("|")),
                    lineas,
                )
            )

            return movs
        except:
            return []


def movimientoDesdeStdout(datos: list[str]) -> Movimiento:
    fecha, operacion = datos
    fecha = fecha[fecha.index(":") + 1 :].strip()
    fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
    idOp = -1
    if "extraccion" in operacion:
        idOp = 1
    elif "clave" in operacion:
        idOp = 2

    return Movimiento("-1", idOp, fecha)


"""
EJEMPLO SALIDA MOVIMIENTOS


Consulta de movimientos ok. Movimientos: 

Fecha: 29/11/2023 20:22:54 | Operación: extraccion

Fecha: 29/11/2023 20:22:55 | Operación: extraccion
"""

"""
ESTADO EJEMPLO 
{
    "usuarios": {
        "12345678": "admin_nombre",
        "1": "prueba",
        "2": "prueba"
    },
    "claves": {
        "12345678": "admin123",
        "1": "asdf",
        "2": "asdf"
    },
    "saldos": {
        "12345678": 0,
        "1": 1,
        "2": 1
    },
    "sueldos": {
        "12345678": 0,
        "1": 1,
        "2": 1
    },
    "movimientos": {
        "12345678": {},
        "1": {
            "2023-08-29T20:45:14.1889010-03:00": 1
        },
        "2": {
            "2023-08-29T20:45:14.1889010-03:00": 0
        }
    },
    "saldo": 0
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS


Consulta de movimientos ok. Movimientos: 

Fecha: 29/11/2023 20:22:54  Operación: extraccion

Fecha: 29/11/2023 20:22:55  Operación: extraccion
"""
