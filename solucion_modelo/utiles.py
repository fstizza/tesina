from modelos.movimiento import Movimiento
from tipos import *
from constantes import ahora, clave_administrador, dni_administrador


def mismo_mes(fecha: FECHAHORA):
    return ahora.month == fecha.month and ahora.year == fecha.year


def mismo_dia(fecha: FECHAHORA):
    return (
        ahora.day == fecha.day
        and ahora.month == fecha.month
        and ahora.year == fecha.year
    )


def es_administrador(dni: DNI, clave: CLAVE) -> bool:
    return dni == dni_administrador and clave == clave_administrador


def contiene_letras_numeros(clave: CLAVE) -> bool:
    contiene_letra = any(c.isalpha() for c in clave)
    contiene_numero = any(c.isdigit() for c in clave)

    return contiene_letra and contiene_numero


def cantidad_extracciones_usuario_hoy(dni: DNI, movimientos: list[Movimiento]) -> int:
    movimientos_usuario = filter(
        lambda m: m.dni == dni and m.operacion == OPERACION.EXTRACCION, movimientos
    )
    movimientos_usuario_hoy = filter(
        lambda m: mismo_dia(m.fechahora), movimientos_usuario
    )
    return len(list(movimientos_usuario_hoy))


def cantidad_cambios_clave_usuario_mes(dni: DNI, movimientos: list[Movimiento]) -> int:
    movimientos_clave_usuario = filter(
        lambda m: m.dni == dni and m.operacion == OPERACION.CLAVE,
        movimientos,
    )
    movimientos_usuario_mes = filter(
        lambda m: mismo_mes(m.fechahora),
        movimientos_clave_usuario,
    )
    return len(list(movimientos_usuario_mes))
