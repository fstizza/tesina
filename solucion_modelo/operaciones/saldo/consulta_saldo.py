from operaciones.saldo.parametros_consulta_saldo import ParametrosConsultaSaldo
from tipos import *
from estado import Estado


def consulta_saldo(solicitud: ParametrosConsultaSaldo):
    estado = Estado()

    if solicitud.dni not in estado.usuarios.keys():
        return RESULTADO.UsuarioInexistente

    if estado.usuarios[solicitud.dni].clave != solicitud.clave:
        return RESULTADO.ClaveIncorrecta

    saldo = estado.usuarios[solicitud.dni].saldo

    print(f"El saldo del usuario DNI {solicitud.dni} es: {saldo}")

    return RESULTADO.OK
