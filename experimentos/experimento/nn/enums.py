from enum import Enum

class OPERACION(Enum):
    extraccion = 0
    clave = 1

class RESULTADO(str, Enum):
    ok = "ok"
    clave = "clave"
    usuarioInexistente = "usuarioInexistente"
    usuarioYaExistente = "usuarioYaExistente"
    claveIncorrecta = "claveIncorrecta"
    saldoCajeroInsuficiente = "saldoCajeroInsuficiente"
    saldoInsuficiente = "saldoInsuficiente"
    noCumplePoliticaExtraccion = "noCumplePoliticaExtraccion"
    noCumplePoliticaExtraccion2 = "noCumplePoliticaExtraccion2"
    usuarioNoHabilitado = "usuarioNoHabilitado"
    limiteUsuariosAlcanzado = "limiteUsuariosAlcanzado"
    cambioDeClaveBloqueado = "cambioDeClaveBloqueado"
    noCumpleRequisitosClave1 = "noCumpleRequisitosClave1"
    noCumpleRequisitosClave2 = "noCumpleRequisitosClave2"
