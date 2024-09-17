from modelos.movimiento import Movimiento
from modelos.usuario import Usuario
from modelos.usuario_administrador import obtener_administrador
from tipos import DNI
from json import dump, load


class Estado:
    usuarios: dict[DNI, Usuario]
    saldo: int
    movimientos: list[Movimiento]

    def __init__(self):
        self.__leer()

    def __leer(self):
        try:
            with open("estado.json", "r") as estado_archivo:
                estado_json = load(estado_archivo)

                self.movimientos = list(
                    map(lambda m: Movimiento.desde_json(m), estado_json["movimientos"])
                )

                usuarios = list(
                    map(lambda u: (u["dni"], Usuario(u)), estado_json["usuarios"])
                )

                self.usuarios = {}
                self.usuarios.update(usuarios)

                self.saldo = int(estado_json["saldo"])
        except:
            self.__inicial()
            self.guardar()

    def __inicial(self):
        usuario_administrador = obtener_administrador()
        self.usuarios = {usuario_administrador.dni: usuario_administrador}
        self.saldo = 0
        self.movimientos = []

    def guardar(self):
        with open("estado.json", "w") as estado_archivo:
            dump(
                {
                    "usuarios": list(map(lambda u: u.aJson(), self.usuarios.values())),
                    "movimientos": list(map(lambda m: m.aJson(), self.movimientos)),
                    "saldo": self.saldo,
                },
                estado_archivo,
            )
