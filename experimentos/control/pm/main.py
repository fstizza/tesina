from os import sys
from operaciones import Operaciones


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        Operaciones.extraccion(int(args[1]),args[2],int(args[3]))
    elif args[0] == "clave":
        Operaciones.clave(int(args[1]),args[2],args[3])
    elif args[0] == "saldo":
        Operaciones.saldo(int(args[1]),args[2])
    elif args[0] == "alta":
        Operaciones.alta(int(args[1]),args[2],int(args[3]),args[4],args[5],int(args[6]))
    elif args[0] == "carga":
        Operaciones.carga(int(args[1]),args[2],int(args[3]))
    elif args[0] == "movimientos":
        Operaciones.movimientos(int(args[1]),args[2])
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
