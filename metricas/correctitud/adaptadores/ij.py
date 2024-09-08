import pytz
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime, timezone, timedelta
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, FORMATO_FECHA)


FORMATO_FECHA = "%Y-%m-%dT%H:%M:%S.%f0-03:00"


def mapearUsuario(datos: map) -> (Usuario, list[Movimiento]):
    dni = str(datos["DNI"])
    clave = datos["Clave"]
    nombre = datos["Nombre"]
    sueldo = int(datos["Sueldo"])
    saldo = int(datos["Saldo"])

    movimientos = list(
        map(
            lambda d: mapearMovimiento(d, dni),
            filter(
                lambda o: o["Resultado"] == 0
                and o["TipoOperacion"] == 2
                or o["TipoOperacion"] == 4,
                datos["Operaciones"],
            ),
        ),
    )
    usuario = Usuario(dni, clave, nombre, sueldo, saldo)

    return usuario, movimientos


def mapearMovimiento(datos: map, dni: str) -> Movimiento:
    fecha = parser.parse(datos["FechaOperacion"])
    operacion = datos["TipoOperacion"]
    valor = None
    idOp = -1
    if operacion == 2:
        idOp = 1
        valor = int(datos["Monto"])
    elif operacion == 4:
        idOp = 2
    return Movimiento(dni, idOp, fecha, valor)


def movimientoToJson(mov: Movimiento) -> map:
    return {
        "FechaOperacion": mov.fecha.strftime(FORMATO_FECHA),
        "TipoOperacion": 2 if mov.operacion == 1 else (4 if mov.operacion == 2 else -1),
        "Resultado": 0,
        "Monto": mov.valor if mov.valor is not None else -1,
        "Saldo": 0,
    }


class AdaptadorIJ(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            movimientos = []
            usuarios = []
            for usuario in estado_json["Usuarios"]:
                u, m = mapearUsuario(usuario)
                movimientos.extend(m)
                usuarios.append(u)

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["Saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []

        for usuario in estado.usuarios:
            movimientos_usuario = list(
                map(
                    movimientoToJson,
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos),
                )
            )

            usuarios.append(
                {
                    "DNI": int(usuario.dni),
                    "Nombre": usuario.nombre,
                    "Clave": usuario.clave,
                    "Saldo": usuario.saldo,
                    "Sueldo": usuario.sueldo,
                    "Operaciones": movimientos_usuario,
                }
            )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "Usuarios": usuarios,
                    "Saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "1"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%Y-%m-%d")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            id = salida.index("|")
            lineas = salida[id:].strip().splitlines()
            lineas = lineas[1:]
            movs = []
            for linea in lineas:
                fecha, operacion, monto, _, __ = list(
                    map(
                        lambda d: d.strip().replace(",", "."),
                        filter(lambda l: len(l) > 0, linea.split("|")),
                    )
                )
                fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
                valor = -1
                idOp = -1
                if operacion == "Extraccion":
                    idOp = 1
                    valor = int(float(monto.strip()))
                movs.append(Movimiento("-1", idOp, fecha, valor))

            return movs
        except:
            return []


"""
EJEMPLO ESTADO

{
    "Usuarios": [
        {
            "DNI": 1,
            "Nombre": "Administrador",
            "Clave": "admin",
            "Saldo": 100000,
            "Sueldo": 0,
            "Operaciones": [
                {
                    "FechaOperacion": "2023-11-11T15:26:22.6118071-03:00",
                    "TipoOperacion": 1,
                    "Resultado": 0,
                    "Monto": 100000,
                    "Saldo": 100000
                }
            ]
        },
        {
            "DNI": 41404842,
            "Nombre": "Federico",
            "Clave": "prueba123",
            "Saldo": 7000,
            "Sueldo": 10000,
            "Operaciones": [
                {
                    "FechaOperacion": "2023-11-11T15:25:50.5419139-03:00",
                    "TipoOperacion": 0,
                    "Resultado": 0,
                    "Monto": 10000,
                    "Saldo": 0
                },
                {
                    "FechaOperacion": "2023-11-11T15:27:33.9172542-03:00",
                    "TipoOperacion": 2,
                    "Resultado": 0,
                    "Monto": 1000,
                    "Saldo": 9000
                },
                {
                    "FechaOperacion": "2023-11-11T15:27:36.3681563-03:00",
                    "TipoOperacion": 2,
                    "Resultado": 0,
                    "Monto": 1000,
                    "Saldo": 8000
                },
                {
                    "FechaOperacion": "2023-11-11T15:27:39.1058092-03:00",
                    "TipoOperacion": 2,
                    "Resultado": 0,
                    "Monto": 1000,
                    "Saldo": 7000
                },
                {
                    "FechaOperacion": "2023-11-11T15:27:53.3535993-03:00",
                    "TipoOperacion": 4,
                    "Resultado": 0,
                    "Monto": null,
                    "Saldo": 7000
                }
            ]
        }
    ],
    "Saldo": 100000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

La consulta de movimientos se realizó satisfactoriamente.

| Fecha operación  | Tipo operación       | Movimiento | Resultado            | Saldo    |
| 11/11/2023 15:27 | Extraccion           | 1000,00    | OK                   | 7000,00
| 11/11/2023 15:27 | Extraccion           | 1000,00    | OK                   | 8000,00
| 11/11/2023 15:27 | Extraccion           | 1000,00    | OK                   | 9000,00
| 11/11/2023 15:25 | Alta                 | 10000,00   | OK                   | 0,00
"""
