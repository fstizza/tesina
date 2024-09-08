import pytz
from adaptador import Adaptador
from modelos import Estado, Movimiento, Usuario
from json import load, dump
from datetime import datetime, timezone, timedelta
from dateutil import parser


def formatearFecha(fecha: datetime):
    if fecha is None:
        return None
    return datetime.strftime(fecha, "%Y-%m-%dT%H:%M:%S.%f0-03:00")


def mapearCambioClave(datos):
    dni = str(datos["Dni"])
    fecha = parser.parse(datos["Fecha"])
    return Movimiento(dni, 2, fecha)


def mapearUsuario(estado: map, dni: str) -> Usuario:
    clave = ""
    nombre = ""
    sueldo = -1
    saldo = -1

    if dni in estado["Usuarios"].keys():
        clave = estado["Usuarios"][dni]["HashClave"]
        nombre = estado["Usuarios"][dni]["NombreApellido"]
        sueldo = int(estado["Usuarios"][dni]["SueldoMensual"])

        movimientos_usuario = list(
            map(
                lambda mv: mv["Importe"],
                filter(
                    lambda m: m["NumeroDocumentoTitular"] == int(dni),
                    estado["Movimientos"],
                ),
            )
        )

        saldo = 0 if len(movimientos_usuario) == 0 else sum(movimientos_usuario)

    return Usuario(dni, clave, nombre, sueldo, saldo)


def mapearMovimiento(datos: map):
    fecha = parser.parse(datos["Fecha"])
    dni = str(datos["NumeroDocumentoTitular"])
    importe = int(datos["Importe"])
    return Movimiento(dni, 1, fecha, importe)


class AdaptadorCD(Adaptador):
    def __init__(self):
        pass

    def cargar(self):
        with open("estado.json", encoding="utf-8-sig") as archivo_estado:
            estado_json = load(archivo_estado)

            dnis = estado_json["Usuarios"].keys()

            usuarios = list(map(lambda dni: mapearUsuario(estado_json, dni), dnis))

            cambios_claves = []
            for dni in estado_json["CambiosClave"].keys():
                cambios_claves.extend(
                    list(
                        map(
                            mapearCambioClave,
                            filter(
                                lambda d: d["Exitoso"], estado_json["CambiosClave"][dni]
                            ),
                        )
                    )
                )

            movimientos = cambios_claves

            for dni in dnis:
                movimientos_dni = filter(
                    lambda m: m["NumeroDocumentoTitular"] == int(dni)
                    and m["Tipo"] != 0,
                    estado_json["Movimientos"],
                )
                movimientos.extend(list(map(mapearMovimiento, movimientos_dni)))

            estado = Estado()
            estado.movimientos = movimientos
            estado.usuarios = usuarios
            estado.saldo = int(estado_json["DineroDisponible"])
            return estado

    def guardar(self, estado: Estado):
        usuarios = {}
        movimientos = []
        cambiosClave = {}
        movimientos_saldo_inicial = []

        for usuario in estado.usuarios:
            movimientos_cambio_clave = list(
                map(
                    lambda mv: mv.fecha,
                    filter(
                        lambda m: m.dni == usuario.dni and m.operacion == 2,
                        estado.movimientos,
                    ),
                )
            )

            fecha_ultimo_cambio_clave = (
                None
                if len(movimientos_cambio_clave) == 0
                else max(movimientos_cambio_clave)
            )

            usuarios[usuario.dni] = {
                "NombreApellido": usuario.nombre,
                "NumeroDocumento": int(usuario.dni),
                "SueldoMensual": usuario.sueldo,
                "HashClave": usuario.clave,
                "FechaUltimoCambioClave": formatearFecha(fecha_ultimo_cambio_clave),
                "EsAdministrador": True if usuario.nombre == "__admin" else False,
            }

            cambios_clave_usuario = list(
                map(
                    lambda mov: {
                        "Fecha": formatearFecha(mov.fecha),
                        "Exitoso": True,
                        "Dni": int(usuario.dni),
                        "Motivo": "-",
                    },
                    filter(
                        lambda m: m.dni == usuario.dni and m.operacion == 2,
                        estado.movimientos,
                    ),
                )
            )

            extracciones = list(
                map(
                    lambda mv: mv.valor,
                    filter(
                        lambda m: m.operacion == 1
                        and m.dni == usuario.dni
                        and m.valor is not None,
                        estado.movimientos,
                    ),
                )
            )

            saldo_inicial = usuario.saldo - (
                0 if len(extracciones) == 0 else sum(extracciones)
            )

            if len(cambios_clave_usuario) != 0:
                cambiosClave[usuario.dni] = cambios_clave_usuario

            movimientos_saldo_inicial.append(
                {
                    "Fecha": formatearFecha(datetime.now()),
                    "Tipo": 0,
                    "NumeroDocumentoTitular": int(usuario.dni),
                    "Importe": saldo_inicial,
                }
            )

        movimientos = (
            list(
                map(
                    lambda mov: {
                        "Fecha": formatearFecha(mov.fecha),
                        "Tipo": 1,
                        "NumeroDocumentoTitular": int(mov.dni),
                        "Importe": mov.valor,
                    },
                    filter(lambda m: m.operacion != 2, estado.movimientos),
                )
            )
            + movimientos_saldo_inicial
        )

        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "Usuarios": usuarios,
                    "Movimientos": movimientos,
                    "DineroDisponible": estado.saldo,
                    "CambiosClave": cambiosClave,
                },
                estado_archivo,
            )

    def obtenerUsuarioAdministrador(self):
        DNI_ADMIN = "12345678"
        NOMBRE_ADMIN = "__admin"
        CLAVE_ADMIN = "adm1n1strad0r"
        return Usuario(DNI_ADMIN, CLAVE_ADMIN, NOMBRE_ADMIN, 0, 0)

    def fechaString(self, fecha: datetime) -> str:
        return fecha.strftime("%d/%m/%Y")

    def movimientosDesdeSalida(self, salida: str) -> list:
        try:
            lineas = salida.splitlines()
            lineas = lineas[2:]
            lineas = list(filter(lambda l: "Saldo" not in l and "-" not in l, lineas))
            movimientos = []
            for linea in lineas:
                fecha, tipo, monto = list(
                    map(
                        lambda e: e.strip(),
                        filter(
                            lambda s: len(s) > 0,
                            linea.split("|"),
                        ),
                    )
                )

                fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
                tipo = 1 if "Extraccion" in tipo else -1
                monto = int(float(monto.replace(",", ".")))
                movimientos.append(Movimiento("-1", tipo, fecha, monto))
            return movimientos
        except:
            return []


"""
EJEMPLO ESTADO

{
    "Usuarios": {
        "12345678": {
            "NombreApellido": "__admin",
            "NumeroDocumento": 12345678,
            "SueldoMensual": 0,
            "HashClave": "adm1n1strad0r",
            "FechaUltimoCambioClave": null,
            "EsAdministrador": true
        },
        "1": {
            "NombreApellido": "prueba",
            "NumeroDocumento": 1,
            "SueldoMensual": 1,
            "HashClave": "asdf45678",
            "FechaUltimoCambioClave": "2023-08-30T19:54:39.8438224-03:00",
            "EsAdministrador": false
        }
    },
    "Movimientos": [
        {
            "NumeroDocumentoTitular": 1,
            "Fecha": "2023-08-21T15:57:35.205249-03:00",
            "Tipo": 1,
            "Importe": 1
        },
        {
            "NumeroDocumentoTitular": 1,
            "Fecha": "2023-08-21T15:57:35.205249-03:00",
            "Tipo": 1,
            "Importe": 2
        },
        {
            "NumeroDocumentoTitular": 2,
            "Fecha": "2023-08-21T15:57:35.205249-03:00",
            "Tipo": 1,
            "Importe": 3
        },
        {
            "NumeroDocumentoTitular": 12345678,
            "Fecha": "2023-08-21T15:57:38.523513-03:00",
            "Tipo": 0,
            "Importe": 0
        },
        {
            "NumeroDocumentoTitular": 1,
            "Fecha": "2023-08-21T15:57:38.523513-03:00",
            "Tipo": 0,
            "Importe": 1
        }
    ],
    "DineroDisponible": 0,
    "CambiosClave": {
        "1": [
            {
                "Dni": 1,
                "Fecha": "2023-08-30T19:54:16.6178209-03:00",
                "Exitoso": false,
                "Motivo": "La clave debe tener al menos 8 caracters."
            },
            {
                "Dni": 1,
                "Fecha": "2023-08-30T19:54:33.4716122-03:00",
                "Exitoso": false,
                "Motivo": "La clave debe tener alguna letra"
            },
            {
                "Dni": 1,
                "Fecha": "2023-08-30T19:54:39.8438224-03:00",
                "Exitoso": true,
                "Motivo": null
            }
        ]
    }
}
"""

"""
EJEMPLO SALIDA MOVIMIENTOS

|      Fecha       |       Tipo      |    Importe   |
|------------------|-----------------|--------------|
| 21/08/2023 15:57 | Extraccion      |         1,00 |
| 21/08/2023 15:57 | Extraccion      |         2,00 |
| 21/08/2023 15:57 | SaldoInicial    |         1,00 |
"""
