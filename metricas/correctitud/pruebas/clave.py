from datetime import datetime
from modelos import Estado, Solucion, Usuario, Movimiento
from operacion import ejecutar_operacion


"""
Clave01: Comprueba que el DNI del usuario corresponda a uno existente.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave.
- Se le suministra un DNI correcto pero que no corresponde a un usuario existente.
- Se espera que el estado no cambie.

Clave02: Comprueba que se suministren las credenciales del usuario asociado al DNI suministrado.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave.
- Se le suministra un DNI correspondiente a un usuario existente pero una clave incorrecta.
- Se espera que el estado no cambie.

Clave03: Comprueba que no supere el límite diario de cambios de claves.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave y un único movimiento registrado (cambio de clave del usuario) en el día actual.
- Se le suministra DNI y claves del usuario administrador y una clave corrrecta.
- Se espera que el estado no cambie.

Clave04: Comprueba que la nueva clave suministrada sea de al menos 8 caracteres.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave.
- Se le suministra DNI y claves del usuario administrador y una clave incorrrecta, tiene 6 caracteres.
- Se espera que el estado no cambie.

Clave05: Comprueba que la nueva clave suministrada sea una combinación alfanumérica.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave.
- Se le suministra DNI y claves del usuario administrador y una clave incorrrecta, tiene 9 caracteres pero todos numéricos.
- Se espera que el estado no cambie.

Clave06: Comprueba que se realice un cambio de clave con éxito.
- Inicial: Saldo = 0, un solo usuario, el que desea cambiar la clave.
- Se le suministra DNI y claves del usuario administrador y una clave correcta.
- Se espera que el estado cambie y el usuario del estado final tenga asignada la nueva clave.
"""


def clave01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioInexistente"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", "22222222", usuario.clave, "Clave123"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def clave02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", usuario.dni, usuario.clave + "1", "Clave123"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def clave03(solucion: Solucion) -> list[str]:
    """ERROR: LimiteCambiosClave"""
    fecha = datetime.now()
    saldoInicial = 10000
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    movimiento = Movimiento("11111111", 2, fecha)
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = [movimiento]

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", usuario.dni, usuario.clave, "Clave123"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def clave04(solucion: Solucion) -> list[str]:
    """ERROR: NoCumpleRequisitosClave1"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", usuario.dni, usuario.clave, "prueba"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def clave05(solucion: Solucion) -> list[str]:
    """ERROR: NoCumpleRequisitosClave2"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", usuario.dni, usuario.clave, "123123123"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def clave06(solucion: Solucion) -> list[str]:
    """Realiza un cambio de clave con éxito"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []
    nuevaClave = "Prueba123"

    res = ejecutar_operacion(
        solucion, estadoInicial, "clave", usuario.dni, usuario.clave, nuevaClave
    )

    chequeos = []

    if not res.transiciono():
        chequeos.extend(["No transicionó"])
    if len(res.final.movimientos) != 1:
        chequeos.append("len(res.final.movimientos) != 1")
    elif res.final.movimientos[0].operacion != 2:
        chequeos.append("res.final.movimientos[0].operacion != 2")
    if len(res.final.usuarios) > 0 and res.final.usuarios[0].clave != nuevaClave:
        chequeos.append("res.final.usuarios[0].clave != nuevaClave")

    return chequeos
