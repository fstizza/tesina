from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime


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
    fecha = datetime.fromtimestamp(float(fecha))
    idOp = -1
    if (operacion == "extraccion"):
        idOp = 1
    elif (operacion == "claves"):
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "claves"
    return res


class AdaptadorDF(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(lambda dni: mapearUsuario(estado_json, dni), dnis)
            )

            movimientos = []

            for dni in dnis:
                if dni in estado_json["movimientos"].keys():
                    movimientos_dni = estado_json["movimientos"][dni]
                    movimientos.extend(
                        list(map(lambda m: mapearMovimiento(
                            dni, m), movimientos_dni))
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
            movimientos_usuario = list(
                map(
                    lambda mov: [mov.fecha.timestamp(
                    ), mapearIdOperacionStr(mov.operacion)],
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos)
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
        DNI_ADMIN = "1234"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "12345678"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:

        return str(fecha.timestamp())

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida[salida.index('['):].replace(
                "\r", "").replace("\n", "")
            salida = map(lambda x: x.replace("[", "").replace(
                "]", "").split(","), salida.split("],"))
            salida = list(
                map(lambda a: [(a[0]), a[1].replace("'", "").strip()], salida))
            return list(map(lambda l: mapearMovimiento("-1", l), salida))
        except:
            return []


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "1": "Prueba1"
    },
    "claves": {
        "1": "123"
    },
    "saldos": {
        "1": 18000
    },
    "sueldos": {
        "1": 20000
    },
    "movimientos": {
        "1": [
            [
                1693354722.119257,
                "extraccion"
            ],
            [
                1693354722.21963,
                "extraccion"
            ]
        ]
    },
    "saldo": 18000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Los movimientos son: 
[[1693354722.119257, 'extraccion'], [1693354722.21963, 'extraccion']]
"""
