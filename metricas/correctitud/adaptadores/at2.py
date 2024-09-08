import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime


def mapearUsuario(datos: map, estado: map, admin: bool = False) -> Usuario:
    # No persiste sueldo.
    clave = ""
    nombre = ""
    if admin:
        nombre = "__admin"
    sueldo = -1
    saldo = -1
    dni = ""

    claves = datos.keys()
    if "DNI" in claves:
        dni = str(datos["DNI"])
    if "Clave" in claves:
        clave = str(datos["Clave"])
    if "NyA" in claves:
        nombre = str(datos["NyA"])
    if "Saldo" in claves:
        saldo = int(datos["Saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: map):
    # No distingue tipo de operacion.
    fecha, _ = datos
    fecha = datetime.fromtimestamp(float(fecha))
    idOp = -1
    return Movimiento(str(dni), idOp, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'Extraccion'
    elif (id == 2):
        res = "Cambio password"
    return res


def movimientosUsuario(usuario: Usuario, movimientos: list[Movimiento]) -> list[map]:
    return list(
        map(
            lambda mov: [mov.fecha.timestamp(), -1],
            filter(
                lambda m: m.dni == usuario.dni,
                movimientos
            )
        )
    )


class AdaptadorAT2(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = list(
                map(
                    lambda u: mapearUsuario(u, estado_json),
                    estado_json["Accs"]

                )
            )

            usuarios_adm = list(
                map(
                    lambda u: mapearUsuario(u, estado_json, admin=True),
                    estado_json["AdmAcc"],

                )
            )

            movimientos = []
            for usuario in estado_json["Accs"]:
                movimientos.extend(

                    list(
                        map(
                            lambda m: mapearMovimiento(usuario["DNI"], m),
                            usuario["Hist"]
                        )
                    )
                )

            usuarios = usuarios + usuarios_adm

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["Money"])
            return estado

    def guardar(self, estado: Estado):

        admins = list(
            map(
                lambda a: {
                    "DNI": a.dni,
                    "Clave": a.clave,
                    "Movs": []
                },
                filter(
                    lambda u: u.nombre == "__admin",
                    estado.usuarios
                )
            )
        )

        usuarios = filter(
            lambda u: u.nombre != "__admin",
            estado.usuarios
        )

        usuarios = list(
            map(
                lambda u: {
                    "DNI": int(u.dni),
                    "Clave": u.clave,
                    "NyA": u.nombre,
                    "Saldo": u.saldo,
                    "Hist": movimientosUsuario(u, estado.movimientos)
                },
                estado.usuarios
            )
        )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "Accs": usuarios,
                    "AdmAcc": admins,
                    "Money": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "42325945"
        NOMBRE_ADMIN = "__admin"
        CLAVE_ADMIN = "Password1!"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime('%d-%m-%Y')
    
    def movimientosDesdeSalida(self, salida: str) -> list:
        return []


"""
EJEMPLO ESTADO

{
    "Accs": [
        {
            "DNI": 42325945,
            "Clave": "Password1!",
            "NyA": "__admin",
            "Saldo": 0,
            "Hist": []
        }
    ],
    "AdmAcc": [
        {
            "DNI": "42325945",
            "Clave": "Password1!",
            "Movs": []
        }
    ],
    "Money": "10000"
}
"""
