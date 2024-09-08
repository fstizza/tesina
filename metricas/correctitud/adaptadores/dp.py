import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = '%Y-%m-%dT%H:%M:%S.%fZ'


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


def mapearMovimiento(dni: str, datos):
    fecha, datoOperacion = datos
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    operacion = ""
    if (datoOperacion == "extraccion"):
        operacion = 1
    elif (datoOperacion == "clave"):
        operacion = 2
    return Movimiento(dni, operacion, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "clave"
    return res


class AdaptadorDP(Adaptador):
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
                    movimientos_dni = estado_json["movimientos"][dni].items()
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
            movimientos_usuario = filter(
                lambda m: m.dni == usuario.dni, estado.movimientos)

            movimientos_usuario = {m.fecha.strftime(FORMATO_FECHA): mapearIdOperacionStr(m.operacion)
                                   for m in movimientos_usuario}

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
        DNI_ADMIN = "37041537"
        NOMBRE_ADMIN = "Patricio"
        CLAVE_ADMIN = "123456"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            idInicio = salida.index("[")
            idFin = salida.index("]")
            salida = salida[idInicio+1:idFin].replace('"','')
            movs = salida.split(',')
            return list(map(movimientoDesdeStdout, movs))
        except:
            return []
        

def movimientoDesdeStdout(linea: str) -> Movimiento:
    indiceZ = linea.index("Z")
    fecha= linea[:indiceZ+1].strip()
    op = linea[indiceZ+1:].replace(":", '').strip()
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    if op == "extraccion":
        idOp = 1
    elif op == "clave": 
        idOp = 2
    
    return Movimiento("-1", idOp, fecha)


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "37041537": "Patricio",
        "41404842": "fede"
    },
    "claves": {
        "37041537": "123456",
        "41404842": "fede1234"
    },
    "saldos": {
        "37041537": 0,
        "41404842": 9000
    },
    "sueldos": {
        "37041537": 0,
        "41404842": "10000"
    },
    "movimientos": {
        "37041537": {},
        "41404842": {
            "2023-08-30T22:26:41.327Z": "extraccion"
        }
    },
    "saldo": 300004224526
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

["2023-08-30T22:26:41.327Z: extraccion","2023-08-30T22:26:41.337Z: extraccion"]
"""
