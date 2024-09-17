from datetime import datetime
from enum import Enum


class OPERACION(Enum):
    EXTRACCION = 1
    CLAVE = 2

    def __int__(self):
        return self.value


class RESULTADO(Enum):
    OK = 1
    UsuarioInexistente = 2
    UsuarioYaExistente = 3
    ClaveIncorrecta = 4
    SaldoCajeroInsuficiente = 5
    SaldoInsuficiente = 6
    NoCumplePoliticaExtraccion = 7
    NoCumplePoliticaExtraccionAdelanto = 8
    NoCumplePoliticaAdelanto = 9
    LimiteUsuariosAlcanzado = 10
    CambioDeClaveBloqueado = 11
    UsuarioNoHabilitado = 12
    NoCumpleRequisitosClave1 = 13
    NoCumpleRequisitosClave2 = 14
    ParametrosInvalidos = 15
    Error = 16


DNI = str
CLAVE = str
NOMBRE = str
FECHAHORA = datetime
MONTO = int
