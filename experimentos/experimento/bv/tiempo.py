from datetime import datetime,timedelta

def ahora():
    return datetime.today()

def mismo_mes(fecha1, fecha2):
    mes = (fecha1.month == fecha2.month)
    anio = (fecha1.year == fecha2.year)
    return (mes and anio)

def mismo_dia(fecha1, fecha2):
    mes = (fecha1.month == fecha2.month)
    anio = (fecha1.year == fecha2.year)
    dia = (fecha1.day == fecha2.day)
    return (mes and anio and dia)

def dif_fechas_dias(fecha1, fecha2):
    dif = fecha1 - fecha2
    return dif.days

