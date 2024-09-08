from datetime import datetime
from adaptador_estado_factoria import AdaptadorEstadoFactoria
from modelos import Estado, Solucion, Usuario, Movimiento

from operacion import ejecutar_operacion


"""
Alta01: Comprueba que el DNI del usuario corresponda al administrador.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra un DNI correcto pero que no corresponde al usuario administrador
- Se espera que el estado no cambie.

Alta02: Comprueba que se suministren las credenciales correctas del administrador.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra un DNI correspondiente al usuario administrador pero una clave incorrecta.
- Se espera que el estado no cambie.

Alta03: Comprueba que el sueldo suministrado solo acepte valores positivos.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra DNI y claves del usuario administrador pero el monto del sueldo del usuario a dar de alta negativo.
- Se espera que el estado no cambie.

Alta04: Comprueba que no haya usuarios duplicados.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra DNI y claves del usuario administrador, el resto de los valores del alta son válidos aunque el DNI a dar de alta ya está asociado a un usuario.
- Se espera que el estado no cambie.

Alta05: Comprueba que se realice un alta exitosamente.
- Inicial: Saldo = 0, un solo usuario, el administrador.
- Se le suministra DNI y claves del usuario administrador, el resto de los valores del alta son válidos.
- Se espera que el estado se modifique: se debe agregar un nuevo usuario a la lista con los datos provistos.
"""


def alta01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioNoHabilitado"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    saldoInicial = 0
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    args = [
        "alta",
        administrador.dni + "1",
        administrador.clave + "1",
        "22222222",
        "Clave321",
        "10000",
    ]

    if solucion.require_argumento_saldo:
        args.append("10000")

    res = ejecutar_operacion(solucion, estadoInicial, *args)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def alta02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    args = [
        "alta",
        administrador.dni,
        administrador.clave + "1",
        "12345678",
        "Clave1234",
        "prueba",
        "10000",
    ]

    if solucion.require_argumento_saldo:
        args.append("10000")

    res = ejecutar_operacion(solucion, estadoInicial, *args)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def alta03(solucion: Solucion) -> list[str]:
    """ERROR: Sueldo incorrecto"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    args = [
        "alta",
        administrador.dni,
        administrador.clave,
        "321321",
        "Clave1234",
        "prueba",
        "-10000",
    ]

    if solucion.require_argumento_saldo:
        args.append("10000")

    res = ejecutar_operacion(solucion, estadoInicial, *args)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def alta04(solucion: Solucion) -> list[str]:
    """ERROR: Usuario ya existente"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()
    usuario = Usuario("99999999", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador, usuario]
    estadoInicial.movimientos = []

    args = [
        "alta",
        administrador.dni,
        administrador.clave,
        usuario.dni,
        "Clave1234",
        "prueba",
        "10000",
    ]

    if solucion.require_argumento_saldo:
        args.append("10000")

    res = ejecutar_operacion(solucion, estadoInicial, *args)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def alta05(solucion: Solucion) -> list[str]:
    """Realiza un alta con éxito"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    args = [
        "alta",
        administrador.dni,
        administrador.clave,
        "99999999",
        "Clave1234",
        "prueba",
        "10000",
    ]

    if solucion.require_argumento_saldo:
        args.append("10000")

    res = ejecutar_operacion(solucion, estadoInicial, *args)

    chequeos = []

    if not res.transiciono():
        chequeos.append("No transicionó")
    if len(res.final.usuarios) != 2:
        chequeos.append("len(res.final.usuarios) != 2")
        return chequeos
    usuarios = sorted(res.final.usuarios)
    if usuarios[1].dni != "99999999":
        chequeos.append("res.final.usuarios[1].dni != 99999999")
    if usuarios[1].clave != "Clave1234":
        chequeos.append("res.final.usuarios[1].clave != Clave1234")
    if usuarios[1].sueldo != 10000:
        chequeos.append("res.final.usuarios[1].sueldo != 10000")
    if usuarios[1].saldo != 10000:
        chequeos.append("res.final.usuarios[1].saldo != 10000")

    return chequeos
