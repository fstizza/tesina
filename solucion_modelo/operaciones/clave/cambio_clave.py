from modelos.movimiento import Movimiento
from operaciones.clave.parametros_cambio_clave import ParametrosCambioClave
from tipos import RESULTADO, OPERACION
from estado import Estado
from constantes import CANTIDAD_CAMBIOS_CLAVE_MES, ahora
from utiles import (
    cantidad_cambios_clave_usuario_mes,
    contiene_letras_numeros,
)


def cambio_clave(solicitud: ParametrosCambioClave):

    estado = Estado()

    if solicitud.dni not in estado.usuarios.keys():
        return RESULTADO.UsuarioInexistente

    if estado.usuarios[solicitud.dni].clave != solicitud.clave:
        return RESULTADO.ClaveIncorrecta

    if len(solicitud.nueva_clave) < 8:
        return RESULTADO.NoCumpleRequisitosClave1

    if not contiene_letras_numeros(solicitud.nueva_clave):
        return RESULTADO.NoCumpleRequisitosClave2

    if (
        cantidad_cambios_clave_usuario_mes(solicitud.dni, estado.movimientos)
        > CANTIDAD_CAMBIOS_CLAVE_MES
    ):
        return RESULTADO.CambioDeClaveBloqueado

    estado.usuarios[solicitud.dni].clave = solicitud.nueva_clave

    estado.movimientos.append(Movimiento(ahora, OPERACION.CLAVE, solicitud.dni))

    estado.guardar()

    return RESULTADO.OK
