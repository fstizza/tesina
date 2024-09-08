from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%S.%fZ"


def mapearUsuario(usuario: map, cuenta: map, dni: str) -> Usuario:
    clave = usuario["user"]["password"]
    nombre = usuario["user"]["name"]
    sueldo = cuenta["account"]["account"]["salary"]
    saldo = cuenta["account"]["account"]["balance"]

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: map):
    fecha = datos["date"]
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    valor = int(datos["amount"]) if datos["amount"] is not None else -1
    return Movimiento(dni, 1, fecha, valor)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "clave"
    return res


def movimientoDesdeStdout(linea: str) -> Movimiento:
    fecha, monto = linea.split("|")
    fecha = datetime.strptime(fecha.strip(), FORMATO_FECHA)
    monto = int(monto.split("$")[1])
    return Movimiento("-1", 1, fecha, monto)


class AdaptadorNM(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["users"].keys()

            usuarios = list(
                map(
                    lambda dni: mapearUsuario(
                        estado_json["users"][dni],
                        estado_json["accounts"][dni],
                        dni,
                    ),
                    dnis,
                )
            )

            if (
                estado_json["atm"]["admin"] != ""
                and estado_json["atm"]["password"] != ""
            ):
                usuario_administrador = Usuario(
                    estado_json["atm"]["admin"],
                    estado_json["atm"]["password"],
                    "admin",
                    0,
                    0,
                )

                usuarios.append(usuario_administrador)

            movimientos = []

            for dni in dnis:
                ultimo_cambio_clave = None
                if "lastPasswordChange" in estado_json["users"][dni].keys():
                    ultimo_cambio_clave = estado_json["users"][dni][
                        "lastPasswordChange"
                    ]
                if ultimo_cambio_clave is not None:
                    ultimo_cambio_clave = datetime.strptime(
                        ultimo_cambio_clave, FORMATO_FECHA
                    )
                    movimientos.append(Movimiento(dni, 2, ultimo_cambio_clave))
                for mov in estado_json["accounts"][dni]["movements"]:
                    movimientos.append(mapearMovimiento(dni, mov))

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["atm"]["balance"])
            return estado

    def guardar(self, estado: Estado):
        users = {}
        accounts = {}
        atm = {
            "admin": "",
            "password": "",
            "balance": estado.saldo,
        }

        for usuario in estado.usuarios:
            if usuario.nombre == "admin":
                atm["admin"] = usuario.dni
                atm["password"] = usuario.clave
            else:
                movimientos_usuario = list(
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos)
                )

                cambios_clave = list(
                    filter(
                        lambda m: m.operacion == 2,
                        movimientos_usuario,
                    ),
                )
                ultimo_cambio_clave = (
                    max(cambios_clave) if len(cambios_clave) > 0 else None
                )

                hoy = datetime.now().date()

                movimientos_hoy = len(
                    list(
                        filter(
                            lambda m: m.fecha.date() == hoy,
                            movimientos_usuario,
                        ),
                    )
                )

                fechas_movimientos = list(map(lambda m: m.fecha, movimientos_usuario))

                ultimo_movimiento = (
                    max(fechas_movimientos) if len(fechas_movimientos) > 0 else None
                )

                movimientos_usuario = list(
                    map(
                        lambda m: {
                            "amount": m.valor,
                            "date": m.fecha.strftime(FORMATO_FECHA),
                            "operation": "withdraw",
                        },
                        movimientos_usuario,
                    )
                )

                users[usuario.dni] = {
                    "user": {
                        "name": usuario.nombre,
                        "password": usuario.clave,
                    },
                    "lastPasswordChange": (
                        ultimo_cambio_clave.fecha.strftime(FORMATO_FECHA)
                        if ultimo_cambio_clave is not None
                        else None
                    ),
                }

                accounts[usuario.dni] = {
                    "balance": 0,
                    "salary": 0,
                    "movements": movimientos_usuario,
                    "movementsToday": movimientos_hoy,
                    "lastMovement": (
                        ultimo_movimiento.strftime(FORMATO_FECHA)
                        if ultimo_movimiento is not None
                        else None
                    ),
                    "account": {
                        "balance": 0,
                        "salary": 0,
                        "account": {
                            "balance": usuario.saldo,
                            "salary": usuario.sueldo,
                        },
                    },
                }

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "users": users,
                    "atm": atm,
                    "accounts": accounts,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "00000000"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "changeme"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[1:]
            lineas = list(map(movimientoDesdeStdout, lineas))
            return lineas
        except:
            return []


"""
EJEMPLO ESTADO

{
    "users": {
        "41404842": {
            "user": {
                "name": "Prueba123",
                "password": "Prueba123"
            },
            "lastPasswordChange": "2023-11-06T22:37:46.105Z"
        }
    },
    "atm": {
        "admin": "00000000",
        "password": "changeme",
        "balance": 98000
    },
    "accounts": {
        "41404842": {
            "balance": 0,
            "salary": 0,
            "movements": [
                {
                    "amount": 1000,
                    "date": "2023-11-06T22:37:23.823Z",
                    "operation": "withdraw"
                },
                {
                    "amount": 1000,
                    "date": "2023-11-06T22:37:25.906Z",
                    "operation": "withdraw"
                }
            ],
            "movementsToday": 2,
            "lastMovement": "2023-11-06T22:37:23.823Z",
            "account": {
                "balance": 0,
                "salary": 0,
                "account": {
                    "balance": 8000,
                    "salary": 10000
                }
            }
        }
    }
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Los movimientos de la cuenta son los siguientes: 
2023-11-06T22:37:23.823Z | Retiro: $1000
2023-11-06T22:37:25.906Z | Retiro: $1000
"""
