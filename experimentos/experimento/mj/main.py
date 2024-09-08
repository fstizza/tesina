from os import sys
from estado import Estado
import datetime


def monto_validacion(monto):
    return int(monto)


def fecha_validacion(fecha):
    return datetime.datetime.fromisoformat(fecha)


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    e = Estado.cargar()

    if args[0] == "extraccion":
        print(e.extraccion(args[1], args[2],
              monto_validacion(args[3]))['info'])

    elif args[0] == "clave":
        print(e.clave(args[1], args[2], args[3])['info'])

    elif args[0] == "saldo":
        print(e.consulta_saldo(args[1], args[2])['info'])

    elif args[0] == "alta":
        print(e.alta(args[1], args[2], args[3],
              args[4], monto_validacion(args[6]))['info'])

    elif args[0] == "carga":
        print(e.carga(args[1], args[2], monto_validacion(args[3]))['info'])

    elif args[0] == "movimientos":
        resultado = e.movimientos_entre(args[1], args[2], args[3],
                                        fecha_validacion(args[4]), fecha_validacion(args[5]))
        if resultado['resultado'] == None:
            print(resultado['info'])
        else:
            for movimiento in resultado['resultado']:
                print(movimiento[0], " -------> ", movimiento[1])
    else:
        print("Operación inválida.")
        exit(1)

    e.guardar()


if __name__ == "__main__":
    main(sys.argv[1:])
