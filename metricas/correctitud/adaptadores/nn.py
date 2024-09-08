import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime


def str_to_datetime(date):
    arg_list = map(lambda n: int(n), re.split(r',|\:| |\-|\.', date))

    return datetime(*arg_list)


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
    fecha = str_to_datetime(fecha)
    idOp = -1
    if (operacion == "extraccion"):
        idOp = 1
    elif (operacion == "clave"):
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "clave"
    return res


class AdaptadorNN(Adaptador):
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
                    lambda mov: [str(mov.fecha),
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
        DNI_ADMIN = "40278173"
        NOMBRE_ADMIN = "admin_nombre"
        CLAVE_ADMIN = "0123456789"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime('%Y-%m-%d')

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            json = loads(salida)
            return list(
                map(
                    lambda j: Movimiento(
                        "-1", datetime.strptime(j["fechaHora"], '%Y-%m-%d'), 1 if j["operacion"] == "extraccion" else 2),
                    json
                )
            )
        except:
            return []


"""
EJEMPLO DE ESTADO
{
  "claves": {
    "40278173": "0123456789",
    "41404842": "Fede1234"
  },
  "movimientos": {
    "40278173": [],
    "41404842": [
      [
        "2023-08-29 18:38:04.272949",
        "extraccion"
      ],
      [
        "2023-08-29 18:38:05.272949",
        "extraccion"
      ]
    ]
  },
  "saldo": "99000",
  "saldos": {
    "40278173": 0,
    "41404842": "9000"
  },
  "sueldos": {
    "40278173": 0,
    "41404842": 10000
  },
  "usuarios": {
    "40278173": "admin_nombre",
    "41404842": "FEde"
  }
}
"""


"""
EJEMPLO SALIDA MOVIMIENTOS
[{"fechaHora": "2023-08-29", "operacion": "extraccion"}, {"fechaHora": "2023-08-29", "operacion": "extraccion"}]
"""
