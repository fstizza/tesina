from datetime import datetime
from adaptador_estado_factoria import AdaptadorEstadoFactoria
from modelos import Estado, Solucion, Usuario, Movimiento

from operacion import ejecutar_operacion


"""
Carga01: Comprueba que el DNI del usuario corresponda al administrador.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra un DNI correcto pero que no corresponde al usuario administrador
- Se espera que el estado no cambie.

Carga02: Comprueba que se suministren las credenciales correctas del administrador.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra un DNI correspondiente al usuario administrador pero una clave incorrecta.
- Se espera que el estado no cambie.

Carga03: Comprueba que el saldo a acreditar al cajero sea positivo.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra DNI y claves del usuario administrador pero el monto a acreditar negativo.
- Se espera que el estado no cambie.

Carga04: Comprueba que se realice una carga exitosamente.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra DNI y claves del usuario administrador y un monto de 10000.
- Se espera que el estado se modifique: el saldo del cajero debe ser 10000.

"""


def carga01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioNoHabilitado"""

    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 0
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "carga", "99999999", "ASDF", "10000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def carga02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "carga",
        administrador.dni,
        administrador.clave + "1",
        "10000",
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def carga03(solucion: Solucion) -> list[str]:
    """ERROR: No permite cargar montos negativos"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "carga",
        administrador.dni,
        administrador.clave,
        "-10000",
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def carga04(solucion: Solucion) -> list[str]:
    """Realiza una carga con éxito"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "carga",
        administrador.dni,
        administrador.clave,
        "10000",
    )

    chequeos = []

    if not res.transiciono():
        chequeos.append("No transicionó")
    if res.final.saldo != 10000:
        chequeos.append("res.final.saldo != 10000")

    return chequeos
