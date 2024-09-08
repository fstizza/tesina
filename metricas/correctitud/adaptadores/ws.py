import pytz
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime, timezone, timedelta
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, "%Y-%m-%dT%H:%M:%S.%f0-03:00")


def mapearCambioClave(datos):
    dni = str(datos["Dni"])
    fecha = parser.parse(datos["Fecha"])
    return Movimiento(dni, 2, fecha)


"""

 "admin": {
            "NombreApellido": "admin",
            "SueldoMensual": 1000,
            "Clave": "admin"
        },
        "41404842": {
            "NombreApellido": "federico",
            "SueldoMensual": 1000,
            "Clave": "prueba123"
        }
"""


def mapearUsuario(datos: map, dni: str, saldo) -> Usuario:
    clave = datos["Clave"]
    nombre = datos["NombreApellido"]
    sueldo = int(datos["SueldoMensual"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(extraccion: map, clave: map):
    operacion = -1
    valor = -1
    fecha = None
    dni = ""
    if extraccion is not None:
        fecha = parser.parse(extraccion["Fecha"])
        dni = str(extraccion["DocumentoUsuario"])
        valor = int(extraccion["Monto"])
        operacion = 1
    elif clave is not None:
        fecha = parser.parse(clave["Fecha"])
        dni = str(clave["DocumentoUsuario"])
        operacion = 2

    return Movimiento(dni, operacion, fecha, valor)


def usuarioToJson(usuario: Usuario) -> map:
    return {
        "NombreApellido": usuario.nombre,
        "SueldoMensual": usuario.sueldo,
        "Clave": usuario.clave,
    }


def movimientoToJson(movimiento: Movimiento) -> map:
    json = {
        "Fecha": movimiento.fecha.strftime("%Y-%m-%d"),
        "DocumentoUsuario": movimiento.dni,
    }

    if movimiento.operacion == 1:
        json["Monto"] = movimiento.valor

    return json


class AdaptadorWS(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["Usuarios"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(
                        estado_json["Usuarios"][dni],
                        dni,
                        estado_json["SaldosUsuarios"][dni],
                    ),
                    dnis,
                )
            )

            movimientos = list(
                map(
                    lambda m: mapearMovimiento(m, None),
                    estado_json["HistoricoMovimientos"],
                )
            )

            movimientos += list(
                map(
                    lambda m: mapearMovimiento(None, m),
                    estado_json["HistoricoClaves"],
                )
            )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["SaldoCajero"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}
        saldosUsuarios = {}
        historicoMovimientos = []
        historicoClaves = []

        for usuario in estado.usuarios:
            usuarios[usuario.dni] = usuarioToJson(usuario)
            saldosUsuarios[usuario.dni] = usuario.saldo

            historicoClaves = list(
                map(
                    movimientoToJson,
                    filter(
                        lambda m: m.dni == usuario.dni and m.operacion == 2,
                        estado.movimientos,
                    ),
                )
            )

            historicoMovimientos = list(
                map(
                    movimientoToJson,
                    filter(
                        lambda m: m.operacion == 1 and m.dni == usuario.dni,
                        estado.movimientos,
                    ),
                )
            )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "Usuarios": usuarios,
                    "SaldosUsuarios": saldosUsuarios,
                    "HistoricoMovimientos": historicoMovimientos,
                    "HistoricoClaves": historicoClaves,
                    "UsuariosAdmin": ["admin"],
                    "SaldoCajero": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "admin"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d/%m/%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            movs = []
            lineas = salida.splitlines()
            if len(lineas) > 4:
                lineas = lineas[2:-2]
                for linea in lineas:
                    fecha, monto = linea.split(" - ")
                    fecha = datetime.strptime(fecha, "%d/%m/%Y")
                    monto = int(monto)
                    movs.append(Movimiento("-1", 1, fecha, monto))

            return movs
        except:
            return []


"""

EJEMPLO ESTADO

{
    "Usuarios": {
        "admin": {
            "NombreApellido": "admin",
            "SueldoMensual": 1000,
            "Clave": "admin"
        },
        "41404842": {
            "NombreApellido": "federico",
            "SueldoMensual": 1000,
            "Clave": "prueba123"
        }
    },
    "SaldosUsuarios": {
        "41404842": 800
    },
    "HistoricoMovimientos": [
        {
            "Fecha": "2023-11-07",
            "DocumentoUsuario": "41404842",
            "Monto": -100
        },
        {
            "Fecha": "2023-11-07",
            "DocumentoUsuario": "41404842",
            "Monto": -100
        }
    ],
    "HistoricoClaves": [
        {
            "Fecha": "2023-11-07",
            "DocumentoUsuario": "41404842"
        }
    ],
    "UsuariosAdmin": [
        "admin"
    ],
    "SaldoCajero": 150000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Historico de movimiento de la cuenta: 41404842
----------------------------
7/11/2023 - -100
7/11/2023 - -100
----------------------------
Operación finalizada.`
"""
