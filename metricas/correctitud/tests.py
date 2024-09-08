from pruebas.adaptador import pruebaAdaptador
from pruebas.movimientos import *
from pruebas.alta import *
from pruebas.carga import *
from pruebas.extraccion import *
from pruebas.clave import *
from pruebas.saldo import *


def obtener_pruebas(solucion: Solucion, filtro_pruebas: str) -> map:
    pruebas = {
        "pruebaAdaptador": lambda: pruebaAdaptador(solucion),
        "extraccion01": lambda: extraccion01(solucion),
        "extraccion02": lambda: extraccion02(solucion),
        "extraccion03": lambda: extraccion03(solucion),
        "extraccion04": lambda: extraccion04(solucion),
        "extraccion05": lambda: extraccion05(solucion),
        "extraccion06": lambda: extraccion06(solucion),
        "extraccion07": lambda: extraccion07(solucion),
        "extraccion08": lambda: extraccion08(solucion),
        "extraccion09": lambda: extraccion09(solucion),
        "clave01": lambda: clave01(solucion),
        "clave02": lambda: clave02(solucion),
        "clave03": lambda: clave03(solucion),
        "clave04": lambda: clave04(solucion),
        "clave05": lambda: clave05(solucion),
        "clave06": lambda: clave06(solucion),
        "saldo01": lambda: saldo01(solucion),
        "saldo02": lambda: saldo02(solucion),
        "saldo03": lambda: saldo03(solucion),
        "carga01": lambda: carga01(solucion),
        "carga02": lambda: carga02(solucion),
        "carga03": lambda: carga03(solucion),
        "carga04": lambda: carga04(solucion),
        "alta01": lambda: alta01(solucion),
        "alta02": lambda: alta02(solucion),
        "alta03": lambda: alta03(solucion),
        "alta04": lambda: alta04(solucion),
        "alta05": lambda: alta05(solucion),
        "movimientos01": lambda: movimientos01(solucion),
        "movimientos02": lambda: movimientos02(solucion),
        "movimientos03": lambda: movimientos03(solucion),
        "movimientos04": lambda: movimientos04(solucion),
        "movimientos05": lambda: movimientos05(solucion),
        "movimientos06": lambda: movimientos06(solucion),
        "movimientos07": lambda: movimientos07(solucion),
        "movimientos08": lambda: movimientos08(solucion),
    }

    if filtro_pruebas is not None and len(filtro_pruebas) != 0:
        pruebas = {
            key: pruebas[key]
            for key in list(
                filter(lambda k: k.upper().startswith(filtro_pruebas.upper()), pruebas)
            )
        }

    return pruebas
