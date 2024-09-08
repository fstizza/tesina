from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d"


def mapearUsuario(datos: map) -> Usuario:
    dni = str(datos["dni"])
    clave = datos["clave"]
    nombre = datos["nombre"]
    sueldo = int(datos["sueldo"])
    saldo = int(datos["cuenta"]["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: map):
    operacion = datos["tipo"]
    fecha = datetime.fromisoformat(datos["fecha"])
    monto = int(datos["monto"])
    idOp = -1
    if operacion == "DEBITO":
        idOp = 1
    elif operacion == "CAMBIO_CLAVE":
        idOp = 2
    return Movimiento(dni, idOp, fecha, monto)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "DEBITO"
    elif id == 2:
        res = "CAMBIO_CLAVE"
    return res


class AdaptadorML(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = list(
                map(lambda usuario: mapearUsuario(usuario), estado_json["usuarios"])
            )

            movimientos = []

            for usuario in estado_json["usuarios"]:
                movimientos_usuario = usuario["cuenta"]["movimientos"]
                movimientos_usuario = list(
                    map(
                        lambda m: mapearMovimiento(str(usuario["dni"]), m),
                        movimientos_usuario,
                    )
                )
                movimientos.extend(movimientos_usuario)

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["cajero"]["monto"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []
        cajero = {
            "monto": estado.saldo,
        }

        for usuario in estado.usuarios:
            movimientos_usuario = list(
                map(
                    lambda mov: {
                        "fecha": mov.fecha.isoformat(),
                        "tipo": mapearIdOperacionStr(mov.operacion),
                        "monto": mov.valor if mov.valor is not None else 0,
                    },
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos),
                )
            )

            datos = {
                "dni": int(usuario.dni),
                "nombre": usuario.nombre,
                "clave": usuario.clave,
                "sueldo": usuario.sueldo,
                "admin": usuario.nombre == "pepe",
                "cuenta": {
                    "saldo": usuario.saldo,
                    "movimientos": movimientos_usuario,
                },
            }
            usuarios.append(datos)

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "cajero": cajero,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "391238934"
        NOMBRE_ADMIN = "pepe"
        CLAVE_ADMIN = "clave"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida.replace("'", '"')
            datos = loads(salida)

            return list(map(lambda l: mapearMovimiento("-1", l), datos))
        except:
            return []


"""
EJEMPLO ESTADO
{
    "usuarios": [
        {
            "dni": 391238934,
            "nombre": "pepe",
            "clave": "clave",
            "sueldo": 0,
            "admin": true,
            "cuenta": {
                "saldo": 0,
                "movimientos": []
            }
        },
        {
            "dni": 41404842,
            "nombre": "Prueba",
            "clave": "123prueba",
            "sueldo": 10000,
            "admin": false,
            "cuenta": {
                "saldo": 9000,
                "movimientos": [
                    {
                        "monto": 0,
                        "tipo": "CAMBIO_CLAVE",
                        "fecha": "2023-11-03T19:11:35.019200"
                    },
                    {
                        "monto": 1000,
                        "tipo": "DEBITO",
                        "fecha": "2023-11-03T19:11:52.652268"
                    }
                ]
            }
        },
        {
            "dni": 41404843,
            "nombre": "Prueba",
            "clave": "Prueba321",
            "sueldo": 10000,
            "admin": false,
            "cuenta": {
                "saldo": 10000,
                "movimientos": []
            }
        }
    ],
    "cajero": {
        "monto": 109000
    }
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

[{'monto': 0, 'tipo': 'CAMBIO_CLAVE', 'fecha': '2023-11-03T19:11:35.019200'}, {'monto': 1000, 'tipo': 'DEBITO', 'fecha': '2023-11-03T19:11:52.652268'}]
"""
