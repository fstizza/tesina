from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = '%d/%m/%y %H:%M:%S'


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'Extracción'
    elif (id == 2):
        res = "Clave"
    return res


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["usuarios"].keys():
        clave = estado["usuarios"][dni]["clave"]
        sueldo = int(estado["usuarios"][dni]["sueldo"])
        saldo = int(estado["usuarios"][dni]["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: list):
    fecha, operacion = datos
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    if ("Extracc" in operacion):
        idOp = 1
    elif ("Clave" in operacion):
        idOp = 2
    return Movimiento(dni, idOp, fecha)


class AdaptadorMJ(Adaptador):
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
        movimientos = {}

        for usuario in estado.usuarios:
            usuarios[usuario.dni] = {
                'clave': usuario.clave,
                'saldo': usuario.saldo,
                'movimientos': {},
                'sueldo': usuario.sueldo
            }

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
                    "movimientos": movimientos,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "admin"
        NOMBRE_ADMIN = "Federico Stizza"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.isoformat() 

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()

            return list(map(movimientoDesdeStdout, lineas))
        except:
            return []

def movimientoDesdeStdout(linea: str) -> Movimiento:
    indiceGuion = linea.index("-")
    indiceMayor = linea.index(">")
    
    fecha = linea[:indiceGuion].strip()
    operacion = linea[indiceMayor+1:].strip()
    datos = [fecha, operacion]

    return mapearMovimiento("-1", datos)
"""
EJEMPLO ESTADO
{
    "movimientos": {
        "41404842": [
            [
                "29/08/23 20:56:05",
                "Extraccion"
            ]
        ],
        "41456789": []
    },
    "saldo": 41403842,
    "usuarios": {
        "41404842": {
            "clave": "123456fe",
            "movimientos": {},
            "saldo": 9000,
            "sueldo": 10000
        },
        "41456789": {
            "clave": "clavefede",
            "movimientos": {},
            "saldo": 0,
            "sueldo": 0
        }
    }
}
"""

"""
EJEMPLO MOVIMIENTOS
29/08/23 20:56:05  ------->  Extraccion
29/08/23 20:56:05  ------->  Extraccion
"""
