from modelos import Estado, Solucion, Usuario

from operacion import ejecutar_operacion


"""
Saldo01: Comprueba que el DNI del usuario corresponda a uno existente.
- Inicial: Saldo = 0, un solo usuario, el que desea consultar el saldo.
- Se le suministra un DNI correcto pero que no corresponde a un usuario existente.
- Se espera que el estado no cambie.

Saldo02: Comprueba que se suministren las credenciales del usuario asociado al DNI suministrado
- Inicial: Saldo = 0, un solo usuario, el que desea consultar el saldo.
- Se le suministra un DNI correspondiente al usuario pero una clave incorrecta.
- Se espera que el estado no cambie.

Saldo03: Comprueba que la operación imprima por pantalla el saldo del usuario autenticado.
- Inicial: Saldo = 0, un solo usuario con un saldo de 2000, el que desea consultar el saldo.
- Se le suministra un DNI y clave correspondientes al usuario.
- Se espera que el estado no cambie y que en la salida estándar esté presente el número 2000.
"""


def saldo01(solucion: Solucion) -> list[str]:
    """ERROR: UsuarioInexistente"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "saldo", "22222222", usuario.clave
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def saldo02(solucion: Solucion) -> list[str]:
    """ERROR: ClaveIncorrecta"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "saldo", usuario.dni, usuario.clave + "1"
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos


def saldo03(solucion: Solucion) -> list[str]:
    """Consulta saldo OK"""
    usuario = Usuario("11111111", "Prueba123", "PRUEBA", 20000, 2000)
    saldoInicial = 10000
    estadoInicial = Estado()
    estadoInicial.saldo = saldoInicial
    estadoInicial.usuarios = [usuario]
    estadoInicial.movimientos = []

    res = ejecutar_operacion(
        solucion, estadoInicial, "saldo", usuario.dni, usuario.clave
    )

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])
    if "2000" not in res.salida:
        chequeos.append('"2000" not in res.salida')

    return chequeos
