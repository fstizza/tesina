from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%d/%m/%Y"


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = estado["clave"]
    nombre = estado["nombre"]
    sueldo = int(estado["sueldo"])
    saldo = int(estado["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


"""
"dni": "1",
                "operacion": "extraccion",
                "monto": 3.0,
                "fecha": "06/11/2023"""


def mapearMovimiento(dni: str, datos: map):
    operacion = datos["operacion"]
    fecha = datos["fecha"]
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    valor = -1
    idOp = -1
    if operacion == "extraccion":
        idOp = 1
        valor = int(datos["monto"])
    elif operacion == "clave":
        idOp = 2
    return Movimiento(dni, idOp, fecha, valor)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "clave"
    return res


def movimientoToJson(movimiento: Movimiento) -> map:
    json = {
        "fecha": movimiento.fecha.strftime(FORMATO_FECHA),
        "operacion": mapearIdOperacionStr(movimiento.operacion),
        "dni": movimiento.dni,
    }

    if movimiento.operacion == 1 and movimiento.valor is not None:
        json["monto"] = movimiento.valor

    return json


def mapearAdmin(datos: map, dni: str) -> Usuario:
    nombre = datos["nombre"]
    clave = datos["clave"]

    return Usuario(dni, clave, nombre, 0, 0)


def movimientoFromStdout(datos: list) -> Movimiento:
    idOp = -1
    valor = -1
    if "extraccion" in datos[0]:
        idOp = 1
        valor = int(datos[2].split(":")[1].strip())
    elif "clave" in datos[0]:
        idOp = 2
    fecha = datetime.strptime(datos[1].split(":")[1].strip(), FORMATO_FECHA)

    return Movimiento("-1", idOp, fecha, valor)


class AdaptadorBM2(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis_usuarios = estado_json["clientes"].keys()

            dnis_admins = estado_json["admins"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(estado_json["clientes"][dni], dni),
                    dnis_usuarios,
                )
            )

            admins = list(
                map(
                    lambda dni: mapearAdmin(estado_json["admins"][dni], dni),
                    dnis_admins,
                )
            )

            usuarios.extend(admins)

            movimientos = []

            for dni in dnis_usuarios:
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
        admins = {}
        movimientos = {}

        for usuario in estado.usuarios:
            if usuario.nombre == "admin":
                admins[usuario.dni] = {
                    "dni": usuario.dni,
                    "nombre": usuario.nombre,
                    "clave": usuario.clave,
                }
            else:
                usuarios[usuario.dni] = {
                    "dni": usuario.dni,
                    "nombre": usuario.nombre,
                    "sueldo": usuario.sueldo,
                    "saldo": usuario.saldo,
                    "clave": usuario.clave,
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
                    "clientes": usuarios,
                    "admins": admins,
                    "movimientos": movimientos,
                    "dinero_disponible": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "-1"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]
            lineas = list(
                map(
                    lambda x: movimientoFromStdout(x.split(",")),
                    lineas,
                )
            )
            return lineas
        except:
            return []


"""
EJEMPLO ESTADO

{
    "clientes": {
        "1": {
            "dni": "1",
            "nombre": "user1",
            "sueldo": 20.0,
            "saldo": 11.0,
            "clave": "claveuser1"
        }
    },
    "admins": {
        "-1": {
            "dni": "-1",
            "nombre": "admin",
            "clave": "admin"
        }
    },
    "movimientos": {
        "1": [
            {
                "dni": "1",
                "operacion": "extraccion",
                "monto": 3.0,
                "fecha": "06/11/2023"
            },
            {
                "dni": "1",
                "operacion": "extraccion",
                "monto": 3.0,
                "fecha": "06/11/2023"
            },
            {
                "dni": "1",
                "operacion": "extraccion",
                "monto": 3.0,
                "fecha": "06/11/2023"
            },
            {
                "dni": "1",
                "operacion": "clave",
                "fecha": "06/11/2023"
            }
        ]
    },
    "dinero_disponible": 100191.0
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Los movimientos del usuario dentro del rango de fechas indicado, son los siguientes: 
Operacion: extraccion, Fecha: 06/11/2023, Monto: 3.0
Operacion: extraccion, Fecha: 06/11/2023, Monto: 3.0
Operacion: extraccion, Fecha: 06/11/2023, Monto: 3.0
Operacion: clave, Fecha: 06/11/2023, Monto: -
"""
