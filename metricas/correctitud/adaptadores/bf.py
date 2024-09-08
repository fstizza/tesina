from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime


def mapearUsuario(json: map, dni: str) -> Usuario:
    clave = json["clave"]
    nombre = json["nombre"]
    sueldo = int(json["sueldo"])
    saldo = int(json["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: list):
    fecha, operacion = datos
    fecha = datetime.fromtimestamp(float(fecha))
    idOp = -1
    if operacion == "extraccion":
        idOp = 1
    elif operacion == "claves":
        idOp = 2
    return Movimiento(dni, idOp, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "extraccion"
    elif id == 2:
        res = "claves"
    return res


class AdaptadorBF(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(lambda dni: mapearUsuario(estado_json["usuarios"][dni], dni), dnis)
            )
            movimientos = []

            for dni in dnis:
                datos_movimientos = estado_json["usuarios"][dni]["movimientos"]
                for fecha in datos_movimientos.keys():
                    datos_movimiento = datos_movimientos[fecha]
                    op = 2 if datos_movimiento["op"] == "cambio_clave" else 1
                    valor = -1
                    if "monto" in datos_movimiento.keys():
                        valor = int(datos_movimiento["monto"])
                    elif "clave_nueva" in datos_movimiento.keys():
                        valor = datos_movimiento["clave_nueva"]
                    fecha = datetime.fromisoformat(fecha)
                    movimientos.append(Movimiento(dni, op, fecha, valor))

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}

        for usuario in estado.usuarios:
            movimientos_usuario = {}
            for movimiento in filter(
                lambda m: m.dni == usuario.dni, estado.movimientos
            ):
                fecha = movimiento.fecha.isoformat()
                datos = {
                    "op": mapearIdOperacionStr(movimiento.operacion),
                }
                if movimiento.operacion == 1:
                    datos["monto"] = movimiento.valor
                elif movimiento.operacion == 2:
                    datos["clave_anterior"] = movimiento.valor
                    datos["clave_nueva"] = movimiento.valor

                movimientos_usuario[fecha] = datos

            usuarios[usuario.dni] = {
                "nombre": usuario.nombre,
                "apellido": usuario.nombre,
                "sueldo": usuario.sueldo,
                "clave": usuario.clave,
                "saldo": usuario.saldo,
                "admin": usuario.nombre == "admin",
                "movimientos": movimientos_usuario,
            }

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "-1"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%Y-%m-%d")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida[salida.index("[") :].replace("\r", "").replace("\n", "")
            movs = loads(salida)
            movimientos = []
            for json in movs:
                for fecha in json.keys():
                    operacion = 1 if json[fecha]["op"] == "extraccion" else 2
                    valor = -1
                    if "monto" in json[fecha].keys():
                        valor = int(json[fecha]["monto"])
                    elif "clave_nueva" in json[fecha].keys():
                        valor = json[fecha]["clave_nueva"]
                    fecha = datetime.fromisoformat(fecha)
                    movimientos.append(Movimiento("-1", operacion, fecha, valor))
            return movimientos
        except:
            return []


"""
EJEMPLO ESTADO

{
    "usuarios": {
        "-1": {
            "nombre": "admin",
            "apellido": "admin",
            "sueldo": 0,
            "clave": "admin",
            "saldo": 0,
            "movimientos": {},
            "admin": true
        },
        "41404842": {
            "nombre": "prueba123",
            "sueldo": 10000,
            "clave": "Prueba123",
            "saldo": 9000,
            "movimientos": {
                "2023-11-02T20:56:54.643691": {
                    "op": "extraccion",
                    "monto": 1000
                },
                "2023-11-02T21:00:50.831417": {
                    "op": "cambio_clave",
                    "clave_anterior": "federico",
                    "clave_nueva": "Prueba123"
                }
            },
            "admin": false
        }
    },
    "saldo": 100000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

Movimientos entre 2023-10-10T00:00:00 : 2023-11-10T00:00:00
[
    {
        "2023-11-02T20:56:54.643691": {
            "op": "extraccion",
            "monto": 1000
        }
    }
]
"""
