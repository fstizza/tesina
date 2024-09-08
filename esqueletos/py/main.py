from os import sys


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        # TODO: Completar.
        pass
    elif args[0] == "clave":
        # TODO: Completar.
        pass
    elif args[0] == "saldo":
        # TODO: Completar.
        pass
    elif args[0] == "alta":
        # TODO: Completar.
        pass
    elif args[0] == "carga":
        # TODO: Completar.
        pass
    elif args[0] == "movimientos":
        # TODO: Completar.
        pass
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
