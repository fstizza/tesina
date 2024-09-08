from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump, loads
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d"


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["cuentas"].keys():
        clave = estado["cuentas"][dni]["password"]
        nombre = "admin" if estado["cuentas"][dni]["es_admin"] else "usuario"
        sueldo = int(estado["cuentas"][dni]["sueldo"])
        saldo = int(estado["cuentas"][dni]["saldo"])

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(dni: str, fecha: str, datos: map):
    operacion = datos["tipo"]
    monto = datos["monto"]
    fecha = datetime.strptime(fecha, FORMATO_FECHA)
    idOp = -1
    if "Ext" in operacion:
        idOp = 1
    elif "clave" in operacion:
        idOp = 2
    return Movimiento(dni, idOp, fecha, monto)


def mapearIdOperacionStr(id: int) -> str:
    res = ""
    if id == 1:
        res = "Extracci\u00f3n"
    elif id == 2:
        res = "Cambio de clave"
    return res


class AdaptadorLE(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["cuentas"].keys()

            usuarios = list(map(lambda dni: mapearUsuario(estado_json, dni), dnis))

            movimientos = []

            for dni in dnis:
                if dni in estado_json["historial"].keys():
                    fechas_movimientos_dni = estado_json["historial"][dni].keys()
                    movs = list(
                        map(
                            lambda f: list(
                                map(
                                    lambda m: mapearMovimiento(dni, f, m),
                                    estado_json["historial"][dni][f],
                                )
                            ),
                            fechas_movimientos_dni,
                        )
                    )

                    movs = [item for row in movs for item in row]

                    movimientos.extend(movs)

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["saldo"])
            return estado

    def guardar(self, estado: Estado):
        cuentas = {}
        historial = {}

        for usuario in estado.usuarios:
            movimientos_usuario = list(
                filter(lambda m: m.dni == usuario.dni, estado.movimientos)
            )

            fechas = list(set(map(lambda m: m.fecha.date(), movimientos_usuario)))
            movimientos_por_fecha = list(
                map(
                    lambda f: (
                        f,
                        list(
                            map(
                                lambda mov: {
                                    "tipo": mapearIdOperacionStr(mov.operacion),
                                    "monto": 0 if mov.valor is None else mov.valor,
                                },
                                list(
                                    filter(
                                        lambda m: m.fecha.date() == f,
                                        movimientos_usuario,
                                    )
                                ),
                            )
                        ),
                    ),
                    fechas,
                )
            )
            historial[usuario.dni] = {}
            for movimiento_por_fecha in movimientos_por_fecha:
                fecha = movimiento_por_fecha[0]
                fecha = fecha.strftime(FORMATO_FECHA)
                historial[usuario.dni][fecha] = movimiento_por_fecha[1]
            ultimo_cambio_clave = 0
            if len(fechas) > 0:
                movimientos_por_fecha_claves = list(
                    filter(
                        lambda mf: any(map(lambda m: "clave" in m["tipo"], mf[1])),
                        movimientos_por_fecha,
                    )
                )
                ordenados = sorted(map(lambda m: m[0], movimientos_por_fecha_claves))
                if len(ordenados) > 0:
                    fecha_ultimoCambio_clave = ordenados[-1]
                    ultimo_cambio_clave = int(
                        datetime(
                            fecha_ultimoCambio_clave.year,
                            fecha_ultimoCambio_clave.month,
                            fecha_ultimoCambio_clave.day,
                        ).timestamp()
                    )

            cuentas[usuario.dni] = {
                "password": usuario.clave,
                "saldo": usuario.saldo,
                "dni": usuario.dni,
                "es_admin": usuario.nombre == "admin",
                "ultimo_cambio_clave": ultimo_cambio_clave,
                "sueldo": usuario.sueldo,
            }

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "cuentas": cuentas,
                    "historial": historial,
                    "saldo": estado.saldo,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "11111111"
        NOMBRE_ADMIN = "admin"
        CLAVE_ADMIN = "admin"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime(FORMATO_FECHA)

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            movimientos = salida.splitlines()
            movimientos_mapeados = []
            fecha_actual = None
            for movimiento in movimientos:
                if movimiento.startswith("Movimientos del"):
                    fecha_actual = datetime.strptime(
                        movimiento[15:-1].strip(), FORMATO_FECHA
                    )
                if movimiento.startswith("Nada"):
                    fecha_actual = None
                elif movimiento.startswith("*"):
                    operacion = 1 if "Ext" in movimiento else 2
                    valor = -1
                    if "Ext" in movimiento:
                        valor = int(movimiento[15:].strip())
                    movimientos_mapeados.append(
                        Movimiento(
                            "-1",
                            operacion,
                            fecha_actual,
                            valor,
                        )
                    )

            return movimientos_mapeados
        except:
            return []


"""
EJEMPLO ESTADO

{
  "saldo": 9910000,
  "historial": {
    "41404842": {
      "2023-11-01": [
        {
          "tipo": "Extracci\u00f3n",
          "monto": 100000
        },
        {
          "tipo": "Cambio de clave",
          "monto": 0
        }
      ]
    }
  },
  "cuentas": {
    "11111111": {
      "password": "admin",
      "saldo": 10000,
      "dni": "11111111",
      "es_admin": true,
      "ultimo_cambio_clave": 0,
      "sueldo": 10000
    },
    "41404842": {
      "password": "federico2",
      "saldo": 900000,
      "nombre": "Fede123",
      "dni": "41404842",
      "es_admin": false,
      "ultimo_cambio_clave": 1698877143,
      "sueldo": 1000000
    }
  }
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS
Movimientos del 2023-10-31:
Nada que reportar
Movimientos del 2023-11-01:
* Extracción de 100000
* Cambio de clave
"""
