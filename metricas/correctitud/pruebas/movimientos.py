from datetime import datetime, timedelta
from adaptador_estado_factoria import AdaptadorEstadoFactoria
from modelos import Estado, Solucion, Usuario, Movimiento
from operacion import ejecutar_operacion

"""
Movimientos01: Comprueba que el DNI del usuario corresponda a uno existente.
- Inicial: Saldo = 0, un solo usuario el administrador.
- Se le suministra un DNI correcto pero que no corresponde a un usuario existente.
- Se espera que el estado no cambie.

Movimientos02: Comprueba que se suministren las credenciales del usuario asociado al DNI suministrado.
- Inicial: Saldo = 0, un solo usuario el administrador.
- Se le suministra un DNI correspondiente a un usuario existente pero una clave incorrecta.
- Se espera que el estado no cambie.

Movimientos03: Comprueba que el sistema detecte que se desea buscar movimentos de un usuario inexistente
- Inicial: Saldo = 0, un solo usuario el administrador.
- Se le suministra credenciales correctas pero un DNI a consultar que no corresponde a un usuario válido.
- Se espera que el saldo del cajero no cambie y tampoco el del usuario y que no presente ningún movimiento en pantall.

Movimientos04: Comprueba que el sistema filtre los movimientos según el dni suministrado
- Inicial: Saldo = 0, el administrador y dos usuarios distintos, el primero con 2 movimientos y el segundo con 1 movimiento.
- Se le suministra credenciales correctas, el dni del primero de los usuarios y un rango de fechas válido.
- Se espera que el saldo del cajero no cambie, tampoco el del usuario pero si que se presenten en la pantalla los datos de los 2 movimientos correspondientes al usuario.

Movimientos05: Comprueba que el sistema filtre los movimientos según el dni y el rango inferior de fechas suministrados
- Inicial: Saldo = 0, el administrador y dos usuarios distintos, el primero con 2 movimientos y el segundo con 1 movimiento.
- Se le suministra credenciales correctas, el dni del primero de los usuarios y una fecha desde posterior a uno de los movimientos del usuario especificado.
- Se espera que el saldo del cajero no cambie, tampoco el del usuario pero si se espera que se presente en pantalla el único movimiento del usuario en el rango de fechas dado.

Movimientos06: Comprueba que el sistema filtre los movimientos según el dni y el rango superior de fechas suministrados
- Inicial: Saldo = 0, el administrador y dos usuarios distintos, el primero con 2 movimientos y el segundo con 1 movimiento.
- Se le suministra credenciales correctas, el dni del primero de los usuarios y una fecha hasta posterior a uno de los movimientos del usuario especificado
- Se espera que el saldo del cajero no cambie, tampoco el del usuario pero si se espera que se presente en pantalla el único movimiento del usuario en el rango de fechas dado.

Movimientos07: Comprueba que el sistema filtre los movimientos según el dni y el rango inferior,superior de fechas suministrados
- Inicial: Saldo = 0, el administrador y dos usuarios distintos, el primero con 3 movimientos y el segundo con 1 movimiento.
- Se le suministra credenciales correctas, el dni del primero de los usuarios y una fecha desde posterior al primer movimiento del usuario y hasta posterior a último de los movimientos del primer usuario autenticado.
- Se espera que el saldo del cajero no cambie, tampoco el del usuario pero si se espera que se presente en pantalla los dos movimientos del usuario en el rango de fechas dado.
 
Movimientos08: Comprueba que el sistema filtre los movimientos según el dni y el rango inferior,superior de fechas suministrados cuando desde es igual a hasta
- Inicial: Saldo = 0, el administrador y dos usuarios distintos, el primero con 3 movimientos y el segundo con 1 movimiento.
- Se le suministra credenciales correctas, el dni del primero de los usuarios y una fecha desde posterior al primer movimiento del usuario y hasta posterior a último de los movimientos del primer usuario autenticado.
- Se espera que el saldo del cajero no cambie, tampoco el del usuario pero si se espera que se presente en pantalla los dos movimientos del usuario en el rango de fechas dado.
"""


def ultimoInstanteFecha(fecha: datetime) -> datetime:
    return fecha.replace(hour=23, minute=59, second=59, microsecond=999999)


def primerInstanteFecha(fecha: datetime) -> datetime:
    return fecha.replace(hour=0, minute=0, second=0, microsecond=0)


def movimientos01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioNoHabilitado"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    usuario = Usuario("22222222", "Prueba123", "PRUEBA", 20000, 2000)

    desde = adaptador.fechaString(datetime(2000, 1, 1))
    hasta = adaptador.fechaString(datetime.now())

    saldoInicial = 0
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        "99999999",
        "Prueba123",
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    if len(movimientos) != 0:
        chequeos.append("len(movimientos) != 0")

    return chequeos


def movimientos02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()
    desde = adaptador.fechaString(datetime(2000, 1, 1))
    hasta = adaptador.fechaString(datetime.now())

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave + "1",
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    if len(movimientos) != 0:
        chequeos.append("len(movimientos) != 0")

    return chequeos


def movimientos03(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioInexistente"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()
    desde = adaptador.fechaString(datetime(2000, 1, 1))
    hasta = adaptador.fechaString(datetime.now())

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [administrador]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave + "1",
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    if len(movimientos) != 0:
        chequeos.append("len(movimientos) != 0")

    return chequeos


def movimientos04(solucion: Solucion) -> list[str]:
    """Filtra por usuario OK"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    ahora = datetime.now()

    desde = adaptador.fechaString(datetime(2000, 1, 1))
    hasta = adaptador.fechaString(ultimoInstanteFecha(ahora))

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [
        administrador,
        Usuario("22222222", "Prueba123", "PRUEBA", 1, 1),
        Usuario("33333333", "Prueba321", "PRUEBA", 1, 1),
    ]
    estadoInicial.movimientos = [
        Movimiento("22222222", 1, ahora - timedelta(days=1), 1),
        Movimiento("22222222", 1, ahora - timedelta(days=1) + timedelta(seconds=1), 2),
        Movimiento("33333333", 1, ahora - timedelta(days=1) + timedelta(seconds=2), 3),
    ]

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave,
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])
    if len(movimientos) != 2:
        chequeos.append("len(movimientos) != 2")

    return chequeos


def movimientos05(solucion: Solucion) -> list[str]:
    """Filtra por usuario y desde OK"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    ahora = datetime.now()
    desde = adaptador.fechaString(primerInstanteFecha(ahora) - timedelta(days=1))
    hasta = adaptador.fechaString(ultimoInstanteFecha(ahora))

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [
        administrador,
        Usuario("22222222", "Prueba123", "PRUEBA", 1, 1),
        Usuario("33333333", "Prueba321", "PRUEBA", 1, 1),
    ]
    estadoInicial.movimientos = [
        Movimiento("22222222", 1, ahora - timedelta(days=2), 1),
        Movimiento("22222222", 1, ahora - timedelta(days=1) + timedelta(seconds=1), 2),
        Movimiento("33333333", 1, ahora - timedelta(days=1) + timedelta(seconds=2), 3),
    ]

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave,
        "22222222",
        desde,
        hasta,
    )

    chequeos = []

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    if len(movimientos) != 1:
        chequeos.append("len(movimientos) != 1")

    return chequeos


def movimientos06(solucion: Solucion) -> list[str]:
    """Filtra por usuario y hasta OK"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    ahora = datetime.now()
    desde = adaptador.fechaString(primerInstanteFecha(ahora) - timedelta(days=10))
    hasta = adaptador.fechaString(ultimoInstanteFecha(ahora - timedelta(days=1)))

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [
        administrador,
        Usuario("22222222", "Prueba123", "PRUEBA", 1, 1),
        Usuario("33333333", "Prueba321", "PRUEBA", 1, 1),
    ]
    estadoInicial.movimientos = [
        Movimiento("22222222", 1, ahora - timedelta(days=2), 1),
        Movimiento("22222222", 1, ahora + timedelta(seconds=1), 2),
        Movimiento("33333333", 1, ahora + timedelta(seconds=2), 3),
    ]

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave,
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])
    if len(movimientos) != 1:
        chequeos.append("len(movimientos) != 1")

    return chequeos


def movimientos07(solucion: Solucion) -> list[str]:
    """Filtra por usuario, desde, hasta OK"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()
    ahora = datetime.now()
    desde = adaptador.fechaString(primerInstanteFecha(ahora) - timedelta(days=3))
    hasta = adaptador.fechaString(ultimoInstanteFecha(ahora - timedelta(days=1)))

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [
        administrador,
        Usuario("22222222", "Prueba123", "PRUEBA", 1, 1),
        Usuario("33333333", "Prueba321", "PRUEBA", 1, 1),
    ]
    estadoInicial.movimientos = [
        Movimiento("22222222", 1, ahora - timedelta(days=4), 1),
        Movimiento("22222222", 1, ahora - timedelta(days=2), 2),
        Movimiento("22222222", 1, ahora + timedelta(seconds=1), 3),
        Movimiento("33333333", 1, ahora + timedelta(seconds=2), 4),
    ]

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave,
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])
    if len(movimientos) != 2:
        chequeos.append("len(movimientos) != 2")

    return chequeos


def movimientos08(solucion: Solucion) -> list[str]:
    """Filtra OK con desde = hasta"""

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    administrador = adaptador.obtenerUsuarioAdministrador()

    ahora = datetime.now()
    desde = adaptador.fechaString(ahora - timedelta(days=1))
    hasta = adaptador.fechaString(ahora - timedelta(days=1))

    estadoInicial = Estado()
    estadoInicial.saldo = 0
    estadoInicial.usuarios = [
        administrador,
        Usuario("22222222", "Prueba123", "PRUEBA", 1, 1),
        Usuario("33333333", "Prueba321", "PRUEBA", 1, 1),
    ]
    estadoInicial.movimientos = [
        Movimiento("22222222", 1, ahora - timedelta(days=1) + timedelta(seconds=1), 1),
        Movimiento("22222222", 1, ahora - timedelta(days=1) + timedelta(seconds=2), 2),
        Movimiento("22222222", 1, ahora + timedelta(seconds=1), 3),
        Movimiento("33333333", 1, ahora + timedelta(seconds=2), 4),
    ]

    res = ejecutar_operacion(
        solucion,
        estadoInicial,
        "movimientos",
        administrador.dni,
        administrador.clave,
        "22222222",
        desde,
        hasta,
    )

    movimientos = adaptador.movimientosDesdeSalida(res.salida)

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])
    if len(movimientos) != 2:
        chequeos.append("len(movimientos) != 2")
    return chequeos
