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


def mapearMovimiento(datos: map, dni: str):
    fecha = parser.parse(datos["Fecha"])
    operacion = str(datos["Tipo"])
    idOp = -1
    if operacion == "Extracción":
        idOp = 1
    elif operacion == "Cambio de clave":
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def movimientoToJson(mov: Movimiento) -> map:
    return {
        "Tipo": "Extracción"
        if mov.operacion == 1
        else ("Cambio de clave" if mov.operacion == 2 else ""),
        "Fecha": mov.fecha.strftime(FORMATO_FECHA),
    }


class AdaptadorSA(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            usuario = None
            if estado_json["DNI"] is not None and estado_json["Clave"] is not None:
                usuario = Usuario(
                    estado_json["DNI"],
                    estado_json["Clave"],
                    estado_json["Nombre"],
                    int(estado_json["Sueldos"]),
                    int(estado_json["Saldo"]),
                )

            usuarios = [usuario] if usuario is not None else []
            movimientos = (
                estado_json["Movimientos"]
                if estado_json["Movimientos"] is not None
                else []
            )
            movimientos = list(
                map(
                    lambda m: mapearMovimiento(m, usuario.dni),
                    movimientos,
                )
            )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["SaldoCajero"])
            return estado

    def guardar(self, estado: Estado):
        movimientos = sorted(estado.movimientos, key=lambda k: k.fecha, reverse=True)
        movimientos_usuario = []
        usuario = None

        for mov in movimientos:
            usuarios_filtrados = list(
                filter(lambda u: u.dni == mov.dni, estado.usuarios)
            )
            if len(usuarios_filtrados) > 0:
                usuario = usuarios_filtrados[0]

                movimientos_usuario = list(
                    map(
                        movimientoToJson,
                        filter(lambda m: m.dni == usuario.dni, estado.movimientos),
                    )
                )
                break

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "SaldoCajero": estado.saldo,
                    "DNI": usuario.dni if usuario is not None else None,
                    "Nombre": usuario.nombre if usuario is not None else None,
                    "Clave": usuario.clave if usuario is not None else None,
                    "Sueldos": usuario.sueldo if usuario is not None else None,
                    "Saldo": usuario.saldo if usuario is not None else None,
                    "Movimientos": movimientos_usuario if usuario is not None else None,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "36005591"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "123456"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d/%m/%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            return list(
                map(lambda m: movimientoDesdeStdout(m.split("|")), salida.splitlines())
            )
        except:
            return []


def movimientoDesdeStdout(datos: list) -> Movimiento:
    fecha, operacion = datos
    fecha = datetime.fromisoformat(fecha)
    operacion = (
        1
        if operacion == "Extracción"
        else (2 if operacion == "Cambio de clave" else -1)
    )
    return Movimiento("-1", operacion, fecha)


"""
EJEMPLO ESTADO
{
    "SaldoCajero": 10000,
    "DNI": "41404842",
    "Nombre": "Federico",
    "Clave": "prueba123",
    "Sueldos": 10000,
    "Saldo": 9000,
    "Movimientos": [
        {
            "Tipo": "Alta",
            "Fecha": "2023-11-13T21:49:23.9157952-03:00"
        },
        {
            "Tipo": "Dep\u00F3sito",
            "Fecha": "2023-11-13T21:49:53.9332215-03:00"
        },
        {
            "Tipo": "Extracci\u00F3n",
            "Fecha": "2023-11-13T21:51:56.6228774-03:00"
        }
    ]
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
13/11/2023 21:49:53|Depósito
13/11/2023 21:51:56|Extracción
"""
