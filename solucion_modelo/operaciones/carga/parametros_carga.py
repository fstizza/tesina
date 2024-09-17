from excepciones import ParametrosInvalidos
from tipos import DNI, CLAVE, MONTO


class ParametrosCarga:
    dni: DNI
    clave: CLAVE
    saldo: MONTO

    def __init__(self, argumentos: list[str]) -> None:
        if (
            len(argumentos) != 3
            or not argumentos[2].isdigit()
            or int(argumentos[2]) <= 0
        ):
            raise ParametrosInvalidos()

        self.dni = argumentos[0]
        self.clave = argumentos[1]
        self.saldo = int(argumentos[2])
