from os import sys

from command import Invoker
from extraccion import Extraccion
from cambio_clave import CambioClave
from consulta_saldo import ConsultaSaldo
from alta_usuario import AltaUsuario
from carga_cajero import CargaCajero
from movimientos import Movimientos


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        inv = Invoker(Extraccion, args)
        pass
    elif args[0] == "clave":
        inv = Invoker(CambioClave, args)
        pass
    elif args[0] == "saldo":
        inv = Invoker(ConsultaSaldo, args)
        pass
    elif args[0] == "alta":
        inv = Invoker(AltaUsuario, args)
        pass
    elif args[0] == "carga":
        inv = Invoker(CargaCajero, args)
        pass
    elif args[0] == "movimientos":
        inv = Invoker(Movimientos, args)
        pass
    else:
        print("Operación inválida.")
        exit(1)

    inv.execute_command()


if __name__ == "__main__":
    main(sys.argv[1:])
