from tipos import DNI, CLAVE
from excepciones import ParametrosInvalidos


class ParametrosCambioClave:
    dni: DNI
    clave: CLAVE
    nueva_clave: CLAVE

    def __init__(self, argumentos: list[str]) -> None:
        if len(argumentos) != 3:
            raise ParametrosInvalidos()

        self.dni = argumentos[0]
        self.clave = argumentos[1]
        self.nueva_clave = argumentos[2]
