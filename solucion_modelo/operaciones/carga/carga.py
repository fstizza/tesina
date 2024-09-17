from operaciones.carga.parametros_carga import ParametrosCarga
from tipos import RESULTADO
from estado import Estado
from utiles import es_administrador


def carga(solicitud: ParametrosCarga):
    if not es_administrador(solicitud.dni, solicitud.clave):
        return RESULTADO.UsuarioNoHabilitado

    estado = Estado()

    estado.saldo += solicitud.saldo

    estado.guardar()

    return RESULTADO.OK
