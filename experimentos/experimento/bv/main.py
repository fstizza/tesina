from os import sys

from ops import *
from movs import mov_to_str2


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        dni = args[1]
        clave = args[2]
        monto = int(args[3])
        res = extraccion(dni, clave, monto)

    elif args[0] == "clave":
        dni = args[1]
        actual = args[2]
        nueva = args[3]
        res = cambio_clave(dni, actual, nueva)

    elif args[0] == "saldo":
        dni = args[1]
        clave = args[2]
        res, saldo = consulta_saldo(dni, clave)
        if (res == Res.OK):
            print("Saldo: ", saldo)

    elif args[0] == "alta":
        dni_admin = args[1]
        clave_admin = args[2]
        dni = args[3]
        clave = args[4]
        nombre = args[5]
        sueldo = int(args[6])
        res = alta_usuario(dni_admin, clave_admin, dni, clave, nombre, sueldo)

    elif args[0] == "carga":
        dni_admin = args[1]
        clave_admin = args[2]
        monto = int(args[3])
        res = carga(dni_admin, clave_admin, monto)

    elif args[0] == "movimientos":
        dni_admin = args[1]
        clave_admin = args[2]
        dni = args[3]
        desde = datetime.strptime(args[4], '%d-%m-%Y')
        hasta = datetime.strptime(args[5], '%d-%m-%Y')
        res, mov = consulta_movimientos(
            dni_admin, clave_admin, dni, desde, hasta)
        if (res == Res.OK):
            print(mov_to_str2(mov))

    else:
        print("Operación inválida.")
        exit(1)

    interpretar_res(res)


if __name__ == "__main__":
    main(sys.argv[1:])
