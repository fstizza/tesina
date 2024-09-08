import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ')


def mapearUsuario(datos: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if "clave" in datos.keys():
        clave = datos["clave"]
    if "nombre" in datos.keys():
        nombre = datos["nombre"]
    if "sueldo" in datos.keys():
        sueldo = int(datos["sueldo"])
    if "saldo" in datos.keys() and datos["saldo"] is not None:
        saldo = int(datos["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: map):
    fecha = datetime.strptime(datos["fechahora"], '%Y-%m-%dT%H:%M:%S.%fZ')
    operacion = datos["operacion"]
    idOp = -1
    if (operacion == "extraccion"):
        idOp = 1
    elif (operacion == "clave"):
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def mapearIdOperacionInt(id: int) -> int:
    res = ""
    if (id == 1):
        res = "extraccion"
    elif (id == 2):
        res = "clave"
    return res


class AdaptadorND(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["cuentas"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(
                        estado_json["cuentas"][dni], dni), dnis
                )
            )

            movimientos = []

            for dni in dnis:
                if dni in estado_json["cuentas"].keys():
                    movimientos_dni = estado_json["cuentas"][dni]["movimientos"]
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
        cuentas = {}

        for usuario in estado.usuarios:
            movimientos_usuario = list(
                map(
                    lambda mov: {
                        "fechahora": formatearFecha(mov.fecha),
                        "operacion": mapearIdOperacionInt(mov.operacion)
                    },
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos)
                )
            )

            cuentas[usuario.dni] = {
                "clave": usuario.clave,
                "nombre": usuario.nombre,
                "sueldo": usuario.sueldo,
                "saldo": usuario.saldo,
                "movimientos": movimientos_usuario
            }

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "cuentas": cuentas,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "40000000"
        NOMBRE_ADMIN = "admin_nombre"
        CLAVE_ADMIN = "ClaveAdmin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida.replace("ok", "").replace('\n', '').strip().replace(
                "fechahora", "'fechahora'").replace("operacion", "'operacion'").replace(' ', '').replace("'", '"')
            movs = loads(salida)
            return list(map(lambda m: mapearMovimiento("-1", m), movs))
        except Exception as e:
            return []


"""
ESTADO EJEMPLO
{
    "cuentas": {
        "41404842": {
            "clave": "123456",
            "nombre": "fede",
            "sueldo": 10000,
            "saldo": -1000,
            "movimientos": [
                {
                    "fechahora": "2023-08-24T01:00:20.664Z",
                    "operacion": "extraccion"
                }
            ]
        }
    },
    "saldo": 41403842
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
[
  { fechahora: '2023-08-25T19:08:08.050267Z', operacion: 'extraccion' },
  { fechahora: '2023-08-25T19:08:08.050267Z', operacion: 'extraccion' },
  { fechahora: '2023-08-26T19:08:08.050267Z', operacion: 'clave' }
]
ok
"""