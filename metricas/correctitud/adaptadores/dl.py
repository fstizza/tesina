from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d"


def mapearUsuario(datos: map, dni: str) -> Usuario:
    clave = datos["clave"]
    nombre = datos["nombre"]
    sueldo = int(datos["sueldo"])
    saldo = int(datos["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


"""
"dni": "41404843",
                "operacion": "extraccion",
                "monto": 1000.0,
                "fecha": "2023-11-30"
                """


def mapearMovimiento(dni: str, datos: map):
    print(datos)
    operacion = datos["operacion"]
    fecha = datos["fecha"]
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    valor = None
    if operacion == "extraccion":
        valor = int(datos["monto"])
        idOp = 1
    elif operacion == "clave":
        idOp = 2
    return Movimiento(dni, idOp, fecha, valor)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "claves"
    return res


class AdaptadorDL(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(estado_json["usuarios"][dni], dni),
                    dnis,
                )
            )

            movimientos = []

            for dni in dnis:
                if dni in estado_json["movimientos"].keys():
                    movimientos_dni = estado_json["movimientos"][dni]
                    movimientos.extend(
                        list(map(lambda m: mapearMovimiento(dni, m), movimientos_dni))
                    )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["dinero_disponible"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}
        movimientos = {}

        for usuario in estado.usuarios:
            usuarios[usuario.dni] = {
                "dni": usuario.dni,
                "nombre": usuario.nombre,
                "clave": usuario.clave,
                "saldo": usuario.saldo,
                "sueldo": usuario.sueldo,
            }
            movimientos_usuario = list(
                map(
                    movimientoToJson,
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos),
                )
            )
            movimientos[usuario.dni] = movimientos_usuario

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "movimientos": movimientos,
                    "dinero_disponible": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "-1"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "clave_admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]

            movs = list(
                map(
                    lambda linea: movimientoDesdeStdout(
                        list(map(lambda l: l.split(":")[1].strip(), linea.split(",")))
                    ),
                    lineas,
                )
            )
            return movs
        except:
            return []


def movimientoDesdeStdout(datos: list) -> Movimiento:
    operacion, fecha, monto = datos
    idOp = -1
    valor = None
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    if operacion == "extraccion":
        idOp = 1
        valor = int(monto)
    elif operacion == "clave":
        idOp = 2

    return Movimiento("-1", idOp, fecha, valor)


def movimientoToJson(mov: Movimiento) -> map:
    json = {
        "dni": mov.dni,
        "operacion": mapearIdOperacionStr(mov.operacion),
        "fecha": mov.fecha.strftime(FORMATO_FECHA),
    }

    if mov.operacion == 1 and mov.valor is not None:
        json["monto"] = mov.valor

    return json


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "-1": {
            "dni": "-1",
            "nombre": "admin",
            "sueldo": 0.0,
            "saldo": 0.0,
            "clave": "clave_admin"
        },
        "41404842": {
            "dni": "41404842",
            "nombre": "federico",
            "sueldo": 10000.0,
            "saldo": 10000.0,
            "clave": "Prueba321"
        },
        "41404843": {
            "dni": "41404843",
            "nombre": "federico",
            "sueldo": 10000.0,
            "saldo": 8000.0,
            "clave": "Prueba123"
        }
    },
    "movimientos": {
        "41404843": [
            {
                "dni": "41404843",
                "operacion": "extraccion",
                "monto": 1000.0,
                "fecha": "2023-11-30"
            },
            {
                "dni": "41404843",
                "operacion": "extraccion",
                "monto": 1000.0,
                "fecha": "2023-11-30"
            },
            {
                "dni": "41404843",
                "operacion": "clave",
                "fecha": "2023-11-30"
            }
        ]
    },
    "dinero_disponible": 99000.0
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Los movimientos del usuario dentro del rango de fechas indicado, son los siguientes: 
Operacion: extraccion, Fecha: 2023-11-29, Monto: 1
Operacion: extraccion, Fecha: 2023-11-29, Monto: 2
Operacion: extraccion, Fecha: 2023-11-30, Monto: 3
Operacion: clave, Fecha: 2023-11-30, Monto: -
"""
