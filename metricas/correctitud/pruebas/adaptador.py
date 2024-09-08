from datetime import datetime
from modelos import Estado, Solucion, Usuario, Movimiento
from util import hoy
from operacion import ejecutar_operacion


def pruebaAdaptador(solucion: Solucion) -> list[str]:
    """Prueba que el adaptador guarde el estado inicial y lo cargue con los mismos datos."""
    if solucion.no_usa_fecha:
        fecha = datetime.min
    else:
        fecha = hoy()

    if solucion.no_usa_sueldo:
        sueldo = -1
    else:
        sueldo = 20000

    if solucion.no_usa_tipo_operacion:
        operacion = -1
    else:
        operacion = 1

    estadoInicial = Estado()
    estadoInicial.saldo = 10000
    estadoInicial.usuarios = [Usuario("11111111", "Prueba123", "PRUEBA", sueldo, 2000)]
    estadoInicial.movimientos = [Movimiento("11111111", operacion, fecha, 1000)]

    res = ejecutar_operacion(solucion, estadoInicial, "")

    chequeos = []

    if res.transiciono():
        chequeos.extend(["Transicionó", *res.delta()])

    return chequeos
