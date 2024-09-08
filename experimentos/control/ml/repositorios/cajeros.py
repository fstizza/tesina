from estado import Estado
from entidades.cajero import Cajero

class RepositorioCajero():
    def cajero(self) -> Cajero:
        estado = Estado.cargar()
        return estado.cajero

    def actualizar(self,cajero):
        estado = Estado.cargar()
        estado.cajero = cajero 
        estado.guardar()
