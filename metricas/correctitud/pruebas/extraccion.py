from datetime import datetime, timedelta
from modelos import Estado, Solucion, Usuario, Movimiento
from operacion import ejecutar_operacion


"""
Extraccion01: Comprueba que el DNI del usuario corresponda a uno existente.
- Inicial: Saldo = 10000, un solo usuario, el que desea realizar extracciones.
- Se le suministra un DNI correcto pero que no a un usuario existente.
- Se espera que el estado no cambie.

Extraccion02: Comprueba que se suministren las credenciales del usuario asociado al DNI suministrado.
- Inicial: Saldo = 10000, un solo usuario, el que desea realizar extracciones.
- Se le suministra un DNI correspondiente a un usuario existente pero una clave incorrecta.
- Se espera que el estado no cambie.

Extraccion03: Comprueba que el sistema limite las extracciones diarias del usuario
- Inicial: Saldo = 10000, un solo usuario, el que desea realizar extracciones y tres movimientos de extracción asociados al usuario.
- Se le suministra credenciales correctas y un monto válido a extraer.
- Se espera que el saldo del cajero no cambie y tampoco el del usuario.

Extraccion04: Comprueba que el sistema limite el monto a extraer del usuario según la política especificada
- Inicial: Saldo = 10000, un solo usuario, el que desea realizar extracciones.
- Se le suministra credenciales correctas y un monto válido a extraer mayor a la mitad del sueldo especificado.
- Se espera que el saldo del cajero no cambie y tampoco el del usuario.

Extraccion06: Comprueba que el sistema no permita realizar extracciones si el usuario no tiene saldo suficiente.
- Inicial: Saldo = 10000, un solo usuario con un saldo total de 2000.
- Se le suministra credenciales correctas y un monto válido a extraer mayor a 2000.
- Se espera que el saldo del cajero no cambie y tampoco el del usuario.

Extraccion07: Comprueba que el sistema realice una extracción exitosamente.
- Inicial: Saldo = 10000, un solo usuario con un saldo total de 2500.
- Se le suministra credenciales correctas y un monto válido menor a la mitad del sueldo y menor a su saldo.
- Se espera que el saldo del cajero y el del usuario disminuyan según el monto especificado. 

Extraccion08: Comprueba que el sistema limite las extracciones diarias del usuario, incrementalmente.
- Inicial: Saldo = 20000, un solo usuario.
- Se le suministra credenciales correctas y un monto de 1000 cuatro veces.
- Se espera que el saldo del cajero y el del usuario disminuyan hasta 17000 y se mantenga así en la última operación.
 
Extraccion09: Comprueba que el sistema no permita realizar extracciones de montos negativos.
- Inicial: Saldo = 20000, un solo usuario.
- Se le suministra credenciales correctas y un monto negativo: -1000.
- Se espera que el saldo del cajero no cambie y tampoco el del usuario.

"""


def extraccion01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioInexistente"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", "22222222", usuario.clave, "1000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave + "1", "1000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion03(solucion: Solucion) -> list[str]:
    """ERROR: LimiteExtracciones"""
    fecha = datetime.now()
    saldoInicial = 10000
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = [
        Movimiento("11111111", 1, fecha + timedelta(seconds=1), 100),
        Movimiento("11111111", 1, fecha + timedelta(seconds=2), 100),
        Movimiento("11111111", 1, fecha + timedelta(seconds=3), 100),
    ]

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion04(solucion: Solucion) -> list[str]:
    """ERROR: LimiteMontoExtraccion"""
    fecha = datetime.today()
    saldoInicial = 50000
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 20000)
    movimiento = Movimiento("11111111", 1, fecha, 100)
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = [movimiento]

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "15000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion05(solucion: Solucion) -> list[str]:
    """ERROR: SaldoCajeroInsuficiente"""
    fecha = datetime.now()
    saldoInicial = 200
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 20000)
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion06(solucion: Solucion) -> list[str]:
    """ERROR: SaldoUsuarioInsuficiente"""
    estadoInicial = Estado()
    saldoInicial = 10000
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "2500"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def extraccion07(solucion: Solucion) -> list[str]:
    """Realiza una extracción OK"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2500)
    estadoInicial = Estado()
    estadoInicial.saldo = 10000
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    chequeos = []
    if res.codigo != 0:
        chequeos.append("res.codigo != 0")
    if not res.transiciono():
        chequeos.append("No transicionó")
    if len(res.final.usuarios) > 0 and res.final.usuarios[0].saldo != 1500:
        chequeos.append("res.final.usuarios[0].saldo != 1500")
    if len(res.final.movimientos) != 1:
        chequeos.append("len(res.final.movimientos) == 1")
    elif res.final.movimientos[0].operacion != 1:
        chequeos.append("res.final.movimientos[0].operacion != 1")

    return chequeos


def extraccion08(solucion: Solucion) -> list[str]:
    """Controla límite extracciones OK"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 20000)
    estadoInicial = Estado()
    estadoInicial.saldo = 20000
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    chequeos = []

    res = ejecutar_operacion(
        solucion, res.final, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    res = ejecutar_operacion(
        solucion, res.final, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    if len(res.final.usuarios) > 0 and res.final.usuarios[0].saldo != 17000:
        chequeos.append("res.final.usuarios[0].saldo != 17000")

    res = ejecutar_operacion(
        solucion, res.final, "extraccion", usuario.dni, usuario.clave, "1000"
    )

    if len(res.final.usuarios) > 0 and res.final.usuarios[0].saldo != 17000:
        chequeos.append("res.final.usuarios[0].saldo != 17000")

    return chequeos


def extraccion09(solucion: Solucion) -> list[str]:
    """ERROR: No puede extraer montos negativos"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 20000)
    estadoInicial = Estado()
    estadoInicial.saldo = 20000
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "extraccion", usuario.dni, usuario.clave, "-1000"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos
