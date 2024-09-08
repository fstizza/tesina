import re
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["claves"].keys():
        clave = estado["claves"][dni]
    if dni in estado["usuarios"].keys():
        nombre = estado["usuarios"][dni]
    if dni in estado["sueldos"].keys():
        sueldo = int(estado["sueldos"][dni])
    if dni in estado["saldos"].keys():
        saldo = int(estado["saldos"][dni])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, datos: list):
    fecha = datos["fechaHora"]
    datoOperacion = datos["operacion"]
    fecha = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ')
    operacion = ""
    if (datoOperacion == "extraccion"):
        operacion = 1
    elif (datoOperacion == "claves"):
        operacion = 2
    return Movimiento(dni, operacion, fecha)


def mapearIdOperacionStr(id: int) -> str:
    res = ''
    if (id == 1):
        res = 'extraccion'
    elif (id == 2):
        res = "claves"
    return res


class AdaptadorBM(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["usuarios"].keys()

            usuarios = list(
                map(lambda dni: mapearUsuario(estado_json, dni), dnis)
            )

            movimientos = []

            for dni in dnis:
                if dni in estado_json["movimientos"].keys():
                    movimientos_dni = estado_json["movimientos"][dni]
                    movimientos.extend(
                        list(map(lambda m: mapearMovimiento(
                            dni, m), movimientos_dni))
                    )

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldo"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}
        claves = {}
        saldos = {}
        sueldos = {}
        movimientos = {}

        for usuario in estado.usuarios:
            usuarios[usuario.dni] = usuario.nombre
            claves[usuario.dni] = usuario.clave
            saldos[usuario.dni] = usuario.saldo
            sueldos[usuario.dni] = usuario.sueldo
            movimientos_usuario = list(
                map(
                    lambda mov: {
                        "fechaHora": datetime.strftime(mov.fecha, '%Y-%m-%dT%H:%M:%S.%fZ'),
                        "operacion": mapearIdOperacionStr(mov.operacion)
                    },
                    filter(lambda m: m.dni == usuario.dni, estado.movimientos)
                )
            )
            movimientos[usuario.dni] = movimientos_usuario

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": usuarios,
                    "claves": claves,
                    "saldos": saldos,
                    "sueldos": sueldos,
                    "movimientos": movimientos,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "42325945"
        NOMBRE_ADMIN = "42325945"
        CLAVE_ADMIN = "Password1!"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            salida = salida.replace("RESULTADO", "").replace('\n', '').strip().replace(
                "fechaHora", "'fechaHora'").replace("operacion", "'operacion'").replace(' ', '').replace("'", '"')
            movs = loads(salida)
            return list(map(lambda m: mapearMovimiento("-1", m), movs))
        except Exception as e:
            return []
