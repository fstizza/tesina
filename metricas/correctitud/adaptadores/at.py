import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ")


def mapearUsuario(datos: map) -> Usuario:
    dni = ""
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if "dni" in datos.keys():
        dni = datos["dni"]
    if "clave" in datos.keys():
        clave = datos["clave"]
    if "nombre" in datos.keys():
        nombre = datos["nombre"]
    if "sueldo" in datos.keys():
        sueldo = int(datos["sueldo"])
    if "saldo" in datos.keys() and datos["saldo"] is not None:
        saldo = int(datos["saldo"])

    return Usuario(str(dni), clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: map):
    dia, mes, ano = datos["fecha"]
    fecha = datetime(ano, mes, dia)
    idOp = -1
    valor = -1
    if "monto" in datos.keys():
        idOp = 1
        valor = int(datos["monto"])
    elif "antigua" in datos.keys():
        idOp = 2
    return Movimiento(str(dni), idOp, fecha, valor)


def mapearMovimientos(dni: str, movimientos: list[map]):
    return list(map(lambda m: mapearMovimiento(dni, m), movimientos))


def mapearIdOperacionInt(id: int) -> int:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "clave"
    return res


def movimientoToJson(mov: Movimiento) -> map:
    if mov.operacion == 1:
        return {
            "monto": mov.valor,
            "fecha": [mov.fecha.day, mov.fecha.month, mov.fecha.year],
        }
    else:
        return {
            "fecha": [mov.fecha.day, mov.fecha.month, mov.fecha.year],
            "antigua": "",
            "actual": "",
        }


def procesarMovimientos(movs: list[Movimiento]):
    ahora = datetime.now()

    hoy = datetime(ahora.year, ahora.month, ahora.day)

    extHoy = list(
        map(
            lambda mov: movimientoToJson(mov),
            filter(lambda m: m.fecha == hoy and m.operacion == 1, movs),
        )
    )

    cambiosClaves = list(
        map(lambda m: m.fecha, filter(lambda m: m.fecha and m.operacion == 2, movs))
    )

    ultCambioClave = {}

    if len(cambiosClaves):
        fecha = max(cambiosClaves)
        ultCambioClave = {
            "fecha": [fecha.day, fecha.month, fecha.year],
            "antigua": "",
            "actual": "",
        }

    movsTotales = list(map(lambda mov: movimientoToJson(mov), movs))

    return extHoy, ultCambioClave, movsTotales


class AdaptadorAT(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = list(map(lambda datos: mapearUsuario(
                datos), estado_json["usuarios"]))

            movsPorUsuario = map(
                lambda u: mapearMovimientos(u["dni"], u["movTotales"]),
                estado_json["usuarios"],
            )

            movimientos = [item for row in movsPorUsuario for item in row]

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["fondos"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []

        for usuario in estado.usuarios:
            if usuario.dni == "admin":
                usuario.dni = "-1"
            movimientos_usuario = list(
                filter(lambda m: m.dni == usuario.dni, estado.movimientos)
            )

            extHoy, ultCambioClave, movsTotales = procesarMovimientos(
                movimientos_usuario
            )

            usuarios.append(
                {
                    "dni": int(usuario.dni),
                    "nombre": usuario.nombre,
                    "sueldo": usuario.sueldo,
                    "clave": usuario.clave,
                    "saldo": usuario.saldo,
                    "ultCambioContr": ultCambioClave,
                    "extHoy": extHoy,
                    "movTotales": movsTotales,
                }
            )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "admin": {
                        "dni": "admin",
                        "clave": "admin"
                    },
                    "usuarios": usuarios,
                    "registrados": len(usuarios),
                    "fondos": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "admin"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d-%m-%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            movs = []
            for linea in salida.splitlines():
                idFecha = linea.index("fecha:")
                idSep = linea.index("-", idFecha + 6)
                d, m, a = list(
                    map(lambda x: int(x), linea[idFecha+6:idSep].strip().split(',')))
                fecha = datetime(a, m, d)
                valor = -1
                op = -1
                if "monto" in linea:
                    op = 1
                    idMonto = linea.index("monto:")
                    idSep = linea.index("-", idMonto+6)
                    monto = linea[idMonto+6:idSep].strip()
                    valor = int(monto)
                elif "antigua" in linea:
                    op = 2
                movs.append(
                    Movimiento("-1", op, fecha, valor)
                )
            return movs
        except Exception as e:
            return []


"""
- movimiento 0: monto: 1 - fecha: 29,10,2023 - 
- movimiento 1: monto: 2 - fecha: 29,10,2023 - 
- movimiento 2: fecha: 30,10,2023 - antigua:  - actual:  - 
"""

"""
ESTADO EJEMPLO
{
  "admin": {
    "dni": "admin",
    "clave": "admin"
  },
  "usuarios": [
    {
      "dni": 41404842,
      "nombre": "federico",
      "sueldo": 10000,
      "clave": "Prueba321",
      "saldo": null,
      "ultCambioContr": {
        "fecha": [
          26,
          10,
          2023
        ],
        "antigua": "Prueba123",
        "nueva": "Prueba321"
      },
      "extHoy": [
        {
          "monto": 1234,
          "fecha": [
            26,
            10,
            2023
          ]
        },
        {
          "monto": 1234,
          "fecha": [
            26,
            10,
            2023
          ]
        },
        {
          "monto": null,
          "fecha": [
            26,
            10,
            2023
          ]
        }
      ],
      "movTotales": [
        {
          "monto": 1234,
          "fecha": [
            26,
            10,
            2023
          ]
        },
        {
          "monto": 1234,
          "fecha": [
            26,
            10,
            2023
          ]
        },
        {
          "monto": null,
          "fecha": [
            26,
            10,
            2023
          ]
        },
        {
          "fecha": [
            26,
            10,
            2023
          ],
          "antigua": "Prueba123",
          "nueva": "Prueba321"
        }
      ]
    }
  ],
  "registrados": 1,
  "fondos": null
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
- movimiento 0: monto: 1234 - fecha: 26,10,2023 - 
- movimiento 1: monto: 1234 - fecha: 26,10,2023 - 
- movimiento 2: monto: null - fecha: 26,10,2023 -
ok
"""
