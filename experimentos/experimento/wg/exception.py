class UsuarioInexistente(Exception):
    pass


class UsuarioYaExistente(Exception):
    pass


class ClaveIncorrecta(Exception):
    pass


class LimiteUsuariosAlcanzado(Exception):
    pass


class SaldoCajeroInsuficiente(Exception):
    pass


class SaldoInsuficiente(Exception):
    pass


class NoCumplePoliticaExtraccion(Exception):
    pass


class CambioDeClaveBloqueado(Exception):
    pass


class NoCumpleRequisitosClave(Exception):
    pass


class UsuarioNoHabilitado(Exception):
    pass
