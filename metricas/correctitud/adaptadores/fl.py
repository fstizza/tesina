import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d"


def mapearMovimiento(dni: str, datos: map):
    datoOperacion = datos["operacion"]
    fecha = datetime.fromtimestamp(float(datos["fecha"]))

    operacion = ""
    if datoOperacion == "extraccion":
        operacion = 1
    elif datoOperacion == "clave":
        operacion = 2
    return Movimiento(dni, operacion, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "clave"
    return res


class AdaptadorFL(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"]
            claves = estado_json["claves"]

            usuarios = []

            movimientos = []

            for id in range(len(dnis)):
                usuarios.append(
                    Usuario(
                        dnis[id],
                        claves[id],
                        "",
                        estado_json["sueldos"][id],
                        estado_json["saldos"][id],
                    )
                )

                movimientos_usuario = list(
                    map(
                        lambda m: mapearMovimiento(dnis[id], m),
                        estado_json["movimientos"][id],
                    )
                )

                movimientos.extend(movimientos_usuario)

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []
        claves = []
        saldos = []
        sueldos = []
        movimientos = []

        for usuario in estado.usuarios:
            usuarios.append(usuario.dni)
            claves.append(usuario.clave)
            saldos.append(usuario.saldo)
            sueldos.append(usuario.sueldo)

            movimientos_usuario = filter(
                lambda m: m.dni == usuario.dni, estado.movimientos
            )

            movimientos_usuario = list(
                map(
                    lambda m: {
                        "operacion": mapearIdOperacionStr(m.operacion),
                        "fecha": int(m.fecha.timestamp()),
                    },
                    movimientos_usuario,
                )
            )

            movimientos.append(movimientos_usuario)

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
        DNI_ADMIN = "39119850"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "Lucas123"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = (
                salida.replace("\n", "")
                .replace("'", '"')
                .replace("operacion:", '"operacion":')
                .replace("fecha:", '"fecha":')
            )
            movs = loads(salida)
            movs = list(
                map(
                    lambda m: Movimiento(
                        "-1",
                        1
                        if m["operacion"] == "extraccion"
                        else (2 if m["operacion"] == "clave" else -1),
                        datetime.fromtimestamp(m["fecha"]),
                    ),
                    movs,
                )
            )
            return movs
        except:
            return []


"""
EJEMPLO ESTADO

{
    "usuarios": [
        "39119850",
        "41404842"
    ],
    "claves": [
        "Lucas123",
        "prueba321"
    ],
    "saldos": [
        7000
    ],
    "sueldos": [
        "10000"
    ],
    "movimientos": [
        [
            {
                "operacion": "extraccion",
                "fecha": 1699482099360
            },
            {
                "operacion": "extraccion",
                "fecha": 1699482359943
            },
            {
                "operacion": "extraccion",
                "fecha": 1699482412390
            },
            {
                "operacion": "clave",
                "fecha": 1699482482690
            }
        ]
    ],
    "saldo": 7000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
[
  { operacion: 'extraccion', fecha: 1699482099360 },
  { operacion: 'extraccion', fecha: 1699482359943 },
  { operacion: 'extraccion', fecha: 1699482412390 },
  { operacion: 'clave', fecha: 1699482482690 }
]
"""
