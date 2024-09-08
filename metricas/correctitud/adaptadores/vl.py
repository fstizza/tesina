import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%S.%fZ"


def mapearUsuario(datos: map) -> (Usuario, list[Movimiento]):
    dni = datos["dniUsuario"]
    clave = datos["claveUsuario"]
    nombre = datos["nombre"]
    sueldo = int(datos["sueldoUsuario"])  # ver
    saldo = datos["saldoUsuario"]
    movimientos = list(map(lambda m: mapearMovimiento(dni, m), datos["movimientos"]))

    return Usuario(dni, clave, nombre, sueldo, saldo), movimientos


def mapearMovimiento(dni: str, datos: map) -> Movimiento:
    datoOperacion = datos["movimiento"]
    fecha = datetime.strptime(datos["fecha"], FORMATO_FECHA)
    operacion = ""
    valor = -1
    if datoOperacion == "Extracción":
        operacion = 1
        valor = datos["monto"]
    elif datoOperacion == "Modificación de clave":
        operacion = 2
    return Movimiento(dni, operacion, fecha, valor)


def movimientoToJson(movimiento: Movimiento) -> map:
    json = {
        "movimiento": mapearIdOperacionStr(movimiento.operacion),
        "fecha": movimiento.fecha.strftime(FORMATO_FECHA),
    }
    if movimiento.operacion == 1:
        json["monto"] = movimiento.valor if movimiento.valor is not None else -1

    return json


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "Extracción"
    elif id == 2:
        res = "Modificación de clave"
    return res


def usuarioToJson(usuario: Usuario, movimientos_usuario: list[Movimiento]) -> map:
    ahora = datetime.now().date()

    extracciones = list(
        filter(
            lambda u: u.operacion == 1 and u.fecha.date() == ahora, movimientos_usuario
        )
    )

    extraccionesHoy = len(extracciones)

    fechaUltimaExtraccion = None
    if extraccionesHoy > 0:
        fechaUltimaExtraccion = max(
            list(map(lambda m: m.fecha, extracciones))
        ).strftime(FORMATO_FECHA)

    claves = list(filter(lambda u: u.operacion == 2, movimientos_usuario))

    fechaModificacionClave = None
    if len(claves) > 0:
        fechaModificacionClave = max(list(map(lambda m: m.fecha, claves))).strftime(
            FORMATO_FECHA
        )

    movimientos_usuario = list(map(movimientoToJson, movimientos_usuario))

    return {
        "dniUsuario": usuario.dni,
        "claveUsuario": usuario.clave,
        "nombre": usuario.nombre,
        "sueldoUsuario": str(usuario.sueldo),
        "saldoUsuario": usuario.saldo,
        "fechaModificacionClave": fechaModificacionClave,
        "fechaUltimaExtraccion": fechaUltimaExtraccion,
        "extraccionesHoy": extraccionesHoy,
        "movimientos": movimientos_usuario,
    }


class AdaptadorVL(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            usuarios = []
            movimientos = []
            for usuario in estado_json["usuarios"]:
                usuario, movimientos_usuario = mapearUsuario(usuario)

                usuarios.append(usuario)
                movimientos.extend(movimientos_usuario)

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldoCajero"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = []

        for usuario in estado.usuarios:
            movimientos_usuario = list(
                filter(
                    lambda m: m.dni == usuario.dni,
                    estado.movimientos,
                ),
            )

            usuarios.append(usuarioToJson(usuario, movimientos_usuario))

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "dniAdmin": "admin",
                    "claveAdmin": "admin",
                    "saldoCajero": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "admin"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"

        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = (
                salida.replace("fecha:", '"fecha":')
                .replace("monto:", '"monto":')
                .replace("movimiento:", '"movimiento":')
                .replace("'", '"')
            )
            datos = loads(salida)
            datos = list(map(lambda m: mapearMovimiento("-1", m), datos))
            return datos
        except:
            return []


"""
EJEMPLO ESTADO

{
    "usuarios": [
        {
            "dniUsuario": "41404842",
            "claveUsuario": "prueba123",
            "nombre": "federico",
            "sueldoUsuario": "100000",
            "saldoUsuario": 98000,
            "fechaModificacionClave": "2023-11-07T21:43:06.487Z",
            "fechaUltimaExtraccion": "2023-11-07T21:42:58.206Z",
            "extraccionesHoy": 2,
            "movimientos": [
                {
                    "fecha": "2023-11-07T21:42:56.726Z",
                    "movimiento": "Extracción",
                    "monto": "1000"
                },
                {
                    "fecha": "2023-11-07T21:42:58.206Z",
                    "movimiento": "Extracción",
                    "monto": "1000"
                },
                {
                    "fecha": "2023-11-07T21:43:06.487Z",
                    "movimiento": "Modificación de clave"
                }
            ]
        }
    ],
    "dniAdmin": "admin",
    "claveAdmin": "admin",
    "saldoCajero": 998000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
[
  {
    fecha: '2023-11-07T21:42:56.726Z',
    movimiento: 'Extracción',
    monto: '1000'
  },
  {
    fecha: '2023-11-07T21:42:58.206Z',
    movimiento: 'Extracción',
    monto: '1000'
  },
  {
    fecha: '2023-11-07T21:43:06.487Z',
    movimiento: 'Modificación de clave'
  }
]
"""
