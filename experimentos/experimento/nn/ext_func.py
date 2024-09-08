from abst_types import FECHAHORA, CLAVE
from enums import OPERACION
import datetime


#def mismo_mes(fecha: FECHAHORA) -> set[FECHAHORA]:
#    import calendar
#
#    num_days = calendar.monthrange(fecha.year, fecha.month)[1]
#    days = [datetime.date(fecha.year, fecha.month, day) for day in range(1, num_days+1)]
#    return days

def subconj_movimientos_mismo_mes(fecha: FECHAHORA, movimientos: set[tuple[FECHAHORA, OPERACION]]) -> set[FECHAHORA]:
    return set([m for m in movimientos if m[0].month == fecha.month and m[0].year == fecha.year])

#def mismo_dia(fecha: FECHAHORA) -> set[FECHAHORA]:
#    pass

def subconj_movimientos_mismo_dia(fecha: FECHAHORA, movimientos: set[tuple[FECHAHORA, OPERACION]]) -> set[FECHAHORA]:
    return set([m for m in movimientos if m[0].day == fecha.day])

def dif_fecha_dias(fecha1: FECHAHORA, fecha2: FECHAHORA) -> set[FECHAHORA]:
    return (fecha2 - fecha1).days

def subconj_movimientos_ventana(desde: FECHAHORA, hasta: FECHAHORA, movimientos: set[tuple[FECHAHORA, OPERACION]]) -> set[FECHAHORA]:
    return set([m for m in movimientos if dif_fecha_dias(desde, m[0]) >= 0 and dif_fecha_dias(m[0], hasta) >= 0])

def longitud(clave: CLAVE) -> int:
    return len(clave)

def contiene_letra_num(clave: set[CLAVE]):
    pass
