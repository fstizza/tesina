import pytz
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime, timezone, timedelta
from dateutil import parser

FORMATO_FECHA = "%d/%m/%Y"


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["usuarios"].keys():
        clave = estado["claves"][dni]
        nombre = estado["usuarios"][dni]
        sueldo = int(estado["sueldos"][dni])
        saldo = int(estado["saldos"][dni])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: list, dni: str):
    fecha, operacion = datos
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    if operacion == "extraccion":
        idOp = 1
    elif operacion == "clave":
        idOp = 2
    return Movimiento(dni, idOp, fecha)


class AdaptadorGF(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(estado_json, dni),
                    dnis,
                )
            )
            movimientos = []
            for usuario in usuarios:
                movimientos_usuario = list(
                    map(
                        lambda mv: mapearMovimiento(mv, usuario.dni),
                        estado_json["movimientos"][usuario.dni],
                    )
                )

                movimientos.extend(movimientos_usuario)

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

            movimientos_usuario = list(
                map(
                    lambda mv: [
                        mv.fecha.strftime(FORMATO_FECHA),
                        "extraccion"
                        if mv.operacion == 1
                        else ("clave" if mv.operacion == 2 else "-1"),
                    ],
                    filter(
                        lambda m: m.dni == usuario.dni,
                        estado.movimientos,
                    ),
                )
            )

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
        DNI_ADMIN = "21354665"
        NOMBRE_ADMIN = "__admin"
        CLAVE_ADMIN = "PASSW0RD"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d/%m/%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            movs = []
            id = salida.index("]") + 1
            salida = salida[:id]
            salida = (
                salida.replace("[", "")
                .replace("]", "")
                .replace("(", "")
                .replace("'", "")
            )
            movs = list(
                filter(
                    lambda z: len(z) != 0,
                    map(
                        lambda x: list(
                            map(
                                lambda zz: zz.strip(),
                                filter(lambda y: y.strip() != "", x.split(",")),
                            )
                        ),
                        salida.split(")"),
                    ),
                )
            )
            return list(map(lambda m: mapearMovimiento(m, "-1"), movs))
        except:
            return []


"""
EJEMPLO ESTADO
{
    "usuarios": {
        "21354665": "ADMIN",
        "41404842": "federico"
    },
    "claves": {
        "21354665": "PASSW0RD",
        "41404842": "Prueb321"
    },
    "saldos": {
        "41404842": 8754
    },
    "sueldos": {
        "41404842": 10000
    },
    "movimientos": {
        "41404842": [
            [
                "08/11/2023",
                "extraccion"
            ],
            [
                "10/11/2023",
                "extraccion"
            ],
            [
                "10/11/2023",
                "extraccion"
            ],
            [
                "10/11/2023",
                "clave"
            ]
        ]
    },
    "saldo": 98754
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
[('08/11/2023', 'extraccion'), ('10/11/2023', 'extraccion'), ('10/11/2023', 'extraccion'), ('10/11/2023', 'clave')]
"""
