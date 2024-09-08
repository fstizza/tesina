from datetime import datetime


class Adaptador:
    def __init__(self) -> None:
        pass

    def cargar(self):
        pass

    def guardar(self, estado) -> None:
        pass

    def obtenerUsuarioAdministrador(self):
        pass

    def fechaString(self, fecha: datetime) -> str:
        pass

    def movimientosDesdeSalida(self, salida: str) -> list:
        pass
