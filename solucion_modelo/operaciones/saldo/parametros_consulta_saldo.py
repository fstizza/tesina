from excepciones import ParametrosInvalidos
from tipos import DNI, CLAVE


class ParametrosConsultaSaldo:
    dni: DNI
    clave: CLAVE

    def __init__(self, argumentos: list[str]) -> None:
        if len(argumentos) != 2:
            raise ParametrosInvalidos()

        self.dni = argumentos[0]
        self.clave = argumentos[1]
