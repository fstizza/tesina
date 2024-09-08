from datetime import datetime
from os import sys

from estado import Estado


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    estado = Estado.cargar()

    if args[0] == "extraccion":
        dni = int(args[1])
        clave = args[2]
        monto = int(args[3])
        estado.extraccion(dni, clave, monto)
    elif args[0] == "clave":
        dni = int(args[1])
        actual = args[2]
        nueva = args[3]
        estado.cambio_clave(dni, actual, nueva)
    elif args[0] == "saldo":
        dni = int(args[1])
        clave = args[2]
        estado.consulta_saldo(dni, clave)
    elif args[0] == "alta":
        dni_adm = int(args[1])
        clave_adm = args[2]
        dni = int(args[3])
        clave = args[4]
        nombre = args[5]
        sueldo = int(args[6])
        saldo = int(args[7])
        estado.alta_usuario(dni_adm, clave_adm, dni, clave, nombre, sueldo, saldo)
    elif args[0] == "carga":
        dni_adm = int(args[1])
        clave_adm = args[2]
        monto = int(args[3])
        estado.carga(dni_adm, clave_adm, monto)
    elif args[0] == "movimientos":
        dni_adm = int(args[1])
        clave_adm = args[2]
        dni_consulta = int(args[3])
        desde = datetime.strptime(args[4], "%d-%m-%Y")
        hasta = datetime.strptime(args[5], "%d-%m-%Y")
        estado.consulta_movimientos(dni_adm, clave_adm, dni_consulta, desde, hasta)
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
