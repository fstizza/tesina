from os import sys
from excepciones import ParametrosInvalidos
from operaciones.alta.parametros_alta_usuario import ParametrosAltaUsuario
from operaciones.carga.parametros_carga import ParametrosCarga
from operaciones.clave.parametros_cambio_clave import ParametrosCambioClave
from operaciones.extraccion.extraccion import extraccion
from operaciones.alta.alta_usuario import alta_usuario
from operaciones.clave.cambio_clave import cambio_clave
from operaciones.carga.carga import carga
from operaciones.extraccion.parametros_extraccion import ParametrosExtraccion
from operaciones.movimientos.parametros_consulta_movimientos import (
    ParametrosConsultaMovimientos,
)
from operaciones.saldo.consulta_saldo import consulta_saldo
from operaciones.movimientos.consulta_movimientos import consulta_movimientos
from operaciones.saldo.parametros_consulta_saldo import ParametrosConsultaSaldo
from tipos import RESULTADO


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    resultado = RESULTADO.Error
    operacion, *argumentos = args

    try:
        if operacion == "extraccion":
            resultado = extraccion(ParametrosExtraccion(argumentos))
        elif operacion == "clave":
            resultado = cambio_clave(ParametrosCambioClave(argumentos))
        elif operacion == "saldo":
            resultado = consulta_saldo(ParametrosConsultaSaldo(argumentos))
        elif operacion == "alta":
            resultado = alta_usuario(ParametrosAltaUsuario(argumentos))
        elif operacion == "carga":
            resultado = carga(ParametrosCarga(argumentos))
        elif operacion == "movimientos":
            resultado = consulta_movimientos(ParametrosConsultaMovimientos(argumentos))
        else:
            print("Operación inválida.")
        print(f"Resultado: {resultado.value}")
    except ParametrosInvalidos:
        print("Parametros invalidos")


if __name__ == "__main__":
    main(sys.argv[1:])
