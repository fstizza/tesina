from os import sys
from cajero import Cajero
from json import dumps
from datetime import datetime as dt

def main(args: list):
    cajero = Cajero()
    
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        # TODO: Completar.
        cajero.extraccion(args[1], args[2], int(args[3]))
    elif args[0] == "clave":
        # TODO: Completar.
        cajero.cambio_clave(args[1], args[2], args[3])
    elif args[0] == "saldo":
        # TODO: Completar.
        saldo = cajero.consulta_saldo(args[1], args[2])
        if saldo is not None:
            print(f'Saldo actual: {saldo}')
    elif args[0] == "alta":
        # TODO: Completar.
        cajero.alta_usuario(args[1], args[2], args[3], args[4], args[5], int(args[6]), int(args[7]))
    elif args[0] == "carga":
        # TODO: Completar.
        cajero.carga_cajero(args[1], args[2], int(args[3]))
    elif args[0] == "movimientos":
        # TODO: Completar.
        try:
            desde = dt.fromisoformat(args[4])
            hasta = dt.fromisoformat(args[5])
        except ValueError as e:
            print('ERROR: formato invalido de fecha, se esperaba el formato aaaa-mm-dd')
            exit(1)
        movs = cajero.consulta_movimientos(args[1], args[2], args[3], desde, hasta)
        print(f'Movimientos entre {desde.isoformat()} : {hasta.isoformat()}')
        print(dumps(movs,indent=4))
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
