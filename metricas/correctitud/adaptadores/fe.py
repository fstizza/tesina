import pytz
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime, timezone, timedelta
from dateutil import parser

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%S.%f0-03:00"


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, FORMATO_FECHA)


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    usuarios = list(
        filter(
            lambda u: u["ValorDNI"] == dni,
            estado["Usuarios"],
        ),
    )
    if len(usuarios) > 0:
        nombre = usuarios[0]["ValorNombre"]

    claves = list(
        filter(
            lambda u: u["ValorDNI"] == dni,
            estado["Claves"],
        ),
    )
    if len(claves) > 0:
        clave = claves[0]["ValorClave"]

    saldos = list(
        filter(
            lambda u: u["ValorDNI"] == dni,
            estado["Saldos"],
        ),
    )
    if len(saldos) > 0:
        saldo = int(saldos[0]["ValorMonto"])

    sueldos = list(
        filter(
            lambda u: u["ValorDNI"] == dni,
            estado["Sueldos"],
        ),
    )
    if len(sueldos) > 0:
        sueldo = int(sueldos[0]["ValorMonto"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: map):
    fecha = parser.parse(datos["FechaHora"]["ValorFechaHora"])
    dni = str(datos["ValorDNI"])
    operacion = 1 if datos["Operacion"] == 0 else (2 if datos["Operacion"] == 2 else -1)
    return Movimiento(dni, operacion, fecha)


class AdaptadorFE(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            movimientos = list(
                map(mapearMovimiento, estado_json["Movimientos"]),
            )

            dnis = list(
                map(
                    lambda u: u["ValorDNI"],
                    estado_json["Usuarios"],
                ),
            )

            usuarios = list(map(lambda dni: mapearUsuario(estado_json, dni), dnis))

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["Saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []
        claves = []
        sueldos = []
        saldos = []
        movimientos = list(map(movimientoToJson, estado.movimientos))

        for usuario in estado.usuarios:
            usuarios.append(
                {
                    "ValorNombre": usuario.nombre,
                    "ValorDNI": usuario.dni,
                }
            )

            claves.append(
                {
                    "ValorClave": usuario.clave,
                    "ValorDNI": usuario.dni,
                }
            )

            sueldos.append(
                {
                    "ValorMonto": usuario.sueldo,
                    "ValorDNI": usuario.dni,
                }
            )
            saldos.append(
                {
                    "ValorMonto": usuario.saldo,
                    "ValorDNI": usuario.dni,
                }
            )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "Usuarios": usuarios,
                    "Claves": claves,
                    "Sueldos": sueldos,
                    "Saldos": saldos,
                    "Movimientos": movimientos,
                    "Saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "administrador"
        NOMBRE_ADMIN = "nombre_administrador"
        CLAVE_ADMIN = "clave_administrador"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%Y-%m-%d")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            movs = []
            lineas = salida.splitlines()
            for linea in lineas:
                operacion, fecha = linea.split("|")
                operacion = operacion.strip()
                fecha = fecha.strip()
                operacion = (
                    1
                    if operacion == "Extraccion"
                    else (2 if operacion == "Clave" else -1)
                )
                fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")

                movs.append(Movimiento("-1", operacion, fecha))

            return movs
        except:
            return []


def movimientoToJson(movimiento: Movimiento) -> map:
    return {
        "FechaHora": {
            "ValorFechaHora": formatearFecha(movimiento.fecha),
        },
        "Operacion": 0
        if movimiento.operacion == 1
        else (1 if movimiento.operacion == 2 else -1),
        "ValorDNI": movimiento.dni,
    }


"""
EJEMPLO ESTADO
{
    "Usuarios": [
        {
            "ValorNombre": "nombre_administrador",
            "ValorDNI": "administrador"
        },
        {
            "ValorNombre": "federico",
            "ValorDNI": "41404842"
        }
    ],
    "Claves": [
        {
            "ValorClave": "clave_administrador",
            "ValorDNI": "administrador"
        },
        {
            "ValorClave": "Prueba321",
            "ValorDNI": "41404842"
        }
    ],
    "Saldos": [
        {
            "ValorMonto": 9800,
            "ValorDNI": "41404842"
        }
    ],
    "Sueldos": [
        {
            "ValorMonto": 10000,
            "ValorDNI": "41404842"
        }
    ],
    "Movimientos": [
        {
            "FechaHora": {
                "ValorFechaHora": "2023-11-08T00:10:42.391954-03:00"
            },
            "Operacion": 0,
            "ValorDNI": "41404842"
        },
        {
            "FechaHora": {
                "ValorFechaHora": "2023-11-08T00:10:44.6199249-03:00"
            },
            "Operacion": 0,
            "ValorDNI": "41404842"
        }
    ],
    "Saldo": 100000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
Extraccion | 8/11/2023 00:10:42
Extraccion | 8/11/2023 00:10:44
"""
