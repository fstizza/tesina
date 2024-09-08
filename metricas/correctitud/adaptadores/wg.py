from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


def mapearUsuario(dni: str, estado: map) -> Usuario:
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
    fecha = datetime.fromtimestamp(fecha)
    idOp = -1
    if operacion == 0:
        idOp = 1
    elif operacion == 1:
        idOp = 2
    return Movimiento(dni, idOp, fecha)


class AdaptadorWG(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(dni, estado_json),
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
                        mv.fecha.timestamp(),
                        0 if mv.operacion == 1 else (1 if mv.operacion == 2 else -1),
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
        DNI_ADMIN = "0"
        NOMBRE_ADMIN = "ADMIN"
        CLAVE_ADMIN = "clave_admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d-%m-%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]
            return list(map(movimientoDesdeStdout, lineas))

        except:
            return []


def movimientoDesdeStdout(linea: str) -> Movimiento:
    fecha, operacion = linea.split("|")
    fecha = datetime.fromisoformat(fecha)
    idOp = -1
    if "extraccion" in operacion:
        idOp = 1
    elif "clave" in operacion:
        idOp = 2
    return Movimiento("-1", idOp, fecha)


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "0": "usr_admin",
        "41404842": "federico"
    },
    "claves": {
        "0": "clave_admin",
        "41404842": "prueba321"
    },
    "movimientos": {
        "41404842": [
            [
                1699665412.201485,
                0
            ],
            [
                1699665413.794709,
                0
            ],
            [
                1699665414.677634,
                0
            ],
            [
                1699665427.675269,
                1
            ]
        ]
    },
    "saldos": {
        "41404842": 970
    },
    "sueldos": {
        "41404842": 1000
    },
    "saldo": 9970
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS 

Fecha     |     Operacion
2023-11-09 22:32:53.167927          Operacion.extraccion
2023-11-09 22:32:54.167927          Operacion.extraccion
2023-11-10 22:32:53.167927          Operacion.extraccion
"""
