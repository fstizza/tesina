from operaciones.movimientos.parametros_consulta_movimientos import (
    ParametrosConsultaMovimientos,
)
from tipos import RESULTADO
from utiles import es_administrador
from estado import Estado


def consulta_movimientos(solicitud: ParametrosConsultaMovimientos):
    if not es_administrador(solicitud.dni, solicitud.clave):
        return RESULTADO.UsuarioNoHabilitado

    estado = Estado()

    if solicitud.dni_consulta not in estado.usuarios.keys():
        return RESULTADO.UsuarioInexistente

    movimientos = filter(
        lambda m: m.fechahora >= solicitud.desde
        and m.fechahora <= solicitud.hasta
        and m.dni == solicitud.dni_consulta,
        estado.movimientos,
    )

    print(f"Movimientos del usuario DNI {solicitud.dni_consulta}")
    for movimiento in movimientos:
        fecha = movimiento.fechahora.strftime("%Y-%m-%d-%H:%M")
        operacion = movimiento.operacion
        print(f"* {fecha} | {operacion}")

    return RESULTADO.OK
