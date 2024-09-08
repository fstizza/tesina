from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = '%m/%d/%Y, %H:%M:%S'


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "cambio_clave"
    return res


def mapearUsuario(datos_cuenta: map, datos_usuario: map) -> Usuario:
    dni = datos_cuenta["dni"]
    clave = datos_cuenta["clave"]
    nombre = datos_usuario["nombre"]
    sueldo = int(datos_usuario["sueldo"])
    saldo = int(datos_cuenta["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: map):

    fecha = datetime.strptime(datos["date"], FORMATO_FECHA)
    operacion = datos["mov_type"]
    dni = datos["dni"]
    valor = -1
    idOp = -1
    if (operacion == "extraccion"):
        idOp = 1
        valor = int(datos["monto"])
    elif (operacion == "cambio_clave"):
        idOp = 2
    return Movimiento(dni, idOp, fecha, valor)


def movimientoToJson(movimiento: Movimiento) -> map:
    datos = {
        "date": movimiento.fecha.strftime(FORMATO_FECHA),
        "mov_type": mapearIdOperacionStr(movimiento.operacion),
        "dni": str(movimiento.dni),
    }

    if movimiento.operacion == 1 and movimiento.valor is not None:
        datos["monto"] = movimiento.valor

    return datos


class AdaptadorMS(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            estado = Estado()

            movimientos = list(
                map(
                    mapearMovimiento,
                    estado_json["mov_list"]
                )
            )

            estado.movimientos = movimientos

            cuentas = estado_json["account_list"]
            usuarios = estado_json["user_list"]

            sorted(cuentas, key=lambda k: k["dni"])
            sorted(usuarios, key=lambda k: k["dni"])

            usuarios = zip(cuentas, usuarios)

            usuarios = list(
                map(
                    lambda t: mapearUsuario(t[0], t[1]),
                    usuarios,
                )
            )

            estado.usuarios = usuarios

            estado.saldo = int(estado_json["saldo_cajero"])

            return estado

    def guardar(self, estado: Estado):
        cuentas = []
        usuarios = []

        movimientos = list(map(movimientoToJson, estado.movimientos))

        for usuario in estado.usuarios:
            usuarios.append({
                "dni": usuario.dni,
                "nombre": usuario.nombre,
                "sueldo": usuario.sueldo
            })
            cuentas.append({
                "dni": usuario.dni,
                "clave": usuario.clave,
                "saldo": usuario.saldo
            })

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "admin_user": "admin",
                    "admin_pass": "pass_admin",
                    "user_list": usuarios,
                    "account_list": cuentas,
                    "mov_list": movimientos,
                    "saldo_cajero": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "admin"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "pass_admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return '"' + fecha.strftime(FORMATO_FECHA) + '"'

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida.replace("'", '"')

            movs = salida.splitlines()

            movs = list(
                map(
                    lambda m: mapearMovimiento(loads(m)),
                    movs
                )
            )

            return movs
        except:
            return []


"""
EJEMPLO ESTADO
{
    "admin_user": "admin",
    "admin_pass": "pass_admin",
    "user_list": [
        {
            "dni": "41404842",
            "nombre": "Prueba123",
            "sueldo": 10000
        }
    ],
    "account_list": [
        {
            "dni": "41404842",
            "clave": "Prueba123",
            "saldo": 9000
        }
    ],
    "mov_list": [
        {
            "mov_type": "extraccion",
            "dni": "41404842",
            "monto": 1000,
            "date": "11/05/2023, 05:05:54"
        },
        {
            "mov_type": "cambio_clave",
            "dni": "41404842",
            "date": "11/05/2023, 05:06:10"
        }
    ],
    "saldo_cajero": 99000
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS 

{'mov_type': 'extraccion', 'dni': '41404842', 'monto': 1000, 'date': '11/05/2023, 05:05:54'}
{'mov_type': 'cambio_clave', 'dni': '41404842', 'date': '11/05/2023, 05:06:10'}

"""
