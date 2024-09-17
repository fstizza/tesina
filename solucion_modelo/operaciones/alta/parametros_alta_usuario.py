from excepciones import ParametrosInvalidos
from tipos import DNI, CLAVE, NOMBRE, MONTO


class ParametrosAltaUsuario:
    dni: DNI
    clave: CLAVE
    dni_usuario: DNI
    clave_usuario: CLAVE
    nombre: NOMBRE
    sueldo: MONTO

    def __init__(self, argumentos: list[str]):
        if (
            len(argumentos) != 6
            or not argumentos[5].isdigit()
            or int(argumentos[5]) <= 0
        ):
            raise ParametrosInvalidos()

        self.dni = argumentos[0]
        self.clave = argumentos[1]
        self.dni_usuario = argumentos[2]
        self.clave_usuario = argumentos[3]
        self.nombre = argumentos[4]
        self.sueldo = int(argumentos[5])
