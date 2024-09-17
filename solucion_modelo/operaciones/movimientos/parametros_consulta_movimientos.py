from tipos import DNI, CLAVE, FECHAHORA
from datetime import datetime
from excepciones import ParametrosInvalidos
from constantes import FORMATO_FECHA


class ParametrosConsultaMovimientos:
    dni: DNI
    clave: CLAVE
    dni_consulta: DNI
    desde: FECHAHORA
    hasta: FECHAHORA

    def __init__(self, argumentos: list[str]) -> None:

        if len(argumentos) != 5:
            raise ParametrosInvalidos()

        self.dni = argumentos[0]
        self.clave = argumentos[1]
        self.dni_consulta = argumentos[2]

        try:
            self.desde = datetime.strptime(argumentos[3], FORMATO_FECHA)
            self.hasta = datetime.strptime(argumentos[4], FORMATO_FECHA)
        except:
            raise ParametrosInvalidos()

        if self.desde > self.hasta:
            raise ParametrosInvalidos()
