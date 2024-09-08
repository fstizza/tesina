from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = '%Y-%m-%d %H:%M:%S'


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "clave"
    return res


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
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    if (operacion == "extraccion"):
        idOp = 1
    elif (operacion == "clave"):
        idOp = 2
    return Movimiento(dni, idOp, fecha)


class AdaptadorBV(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            estado = Estado()

            movimientos = []
            for dni, mov in estado_json["movimientos"].items():
                movimientos.extend(list(
                    map(
                        lambda m: mapearMovimiento(dni, m),
                        mov
                    )
                ))

            estado.movimientos = movimientos

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(lambda dni: mapearUsuario(estado_json, dni), dnis)
            )

            estado.usuarios = usuarios

            estado.saldo = int(estado_json["saldo"])

            return estado

    def guardar(self, estado):
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
                    lambda mov: [datetime.strftime(mov.fecha, FORMATO_FECHA),
                                 mapearIdOperacionStr(mov.operacion)],
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
        DNI_ADMIN = "41456789"
        NOMBRE_ADMIN = "Federico Stizza"
        CLAVE_ADMIN = "clavefede"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime('%d-%m-%Y')

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            id = salida.index("La op")
            salida = salida[:id].strip()
            movs = salida.split(';')
            movs = list(map(lambda m: m.replace(
                '(', '').replace(')', '').replace("'", ""), movs))
            movs = list(map(lambda m: m.split(','), movs))
            movs = list(
                map(lambda m: list(map(lambda mm: mm.strip(), m)), movs))
            return list(map(lambda m: mapearMovimiento("-1", m), movs))
        except:
            return []


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "41456789": "Federico Stizza",
        "1": "prueba",
        "2": "prueba"
    },
    "claves": {
        "41456789": "clavefede",
        "1": "asdf",
        "2": "asdf"
    },
    "saldos": {
        "41456789": 0,
        "1": 1,
        "2": 1
    },
    "sueldos": {
        "41456789": 0,
        "1": 1,
        "2": 1
    },
    "movimientos": {
        "41456789": [],
        "1": [
            [
                "2023-08-20 19:49:52",
                "extraccion"
            ],
            [
                "2023-08-20 19:49:52",
                "extraccion"
            ],
            [
                "2023-08-21 19:49:52",
                "clave"
            ]
        ],
        "2": [
            [
                "2023-08-21 19:49:52",
                "extraccion"
            ]
        ]
    },
    "saldo": 0
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS 

('2023-08-20 19:49:52', 'extraccion');('2023-08-20 19:49:52', 'extraccion');('2023-08-21 19:49:52', 'clave')

"""
