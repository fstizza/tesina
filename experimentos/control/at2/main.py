import time
from os import sys

from estado import Estado


def isIn(accs, clave):
    i = 0
    for d in accs:
        if d['Clave'] == clave:
            return i
        i = i + 1
    return -1


def filterHist(timeMin, timeMax, hist):
    extracts = []
    for h in hist:
        if (h[0] < timeMax) and (h[0] > timeMin):
            extracts.append(h)
    return extracts


def validPass(passwd):
    alpha = 0
    for i in passwd:
        if (i.isalpha()):
            alpha += 1
    return (alpha >= 8) and (len(passwd)-alpha >= 8)


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    e = Estado.cargar()
    if (args[0] == "extraccion"):
        monto = int(args[3])
        position = isIn(e.accs, args[2])
        e.money = int(e.money)
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        elif (e.money >= monto) and (int(e.accs[position]["Saldo"]) >= monto):
            currenttime = time.time()
            if (len(filterHist(0, currenttime, e.accs[position]["Hist"])) >= 2):
                print("Se llegó al límite de extracciones diarias.")
                exit(1)
            else:
                e.money = e.money - monto
                e.accs[position]["Saldo"] = int(
                    e.accs[position]["Saldo"]) - monto
                e.accs[position]["Hist"].append((currenttime, monto))
                e.guardar()
                print("Extracción realizada.")
                exit(1)
        else:
            print("No hay saldo suficiente para efectuar la operación.")
            exit(1)

    elif args[0] == "clave":
        position = isIn(e.accs, args[2])
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        if (not validPass(args[3])):
            print("Contraseña inválida")
            exit(1)
        newkey = isIn(e.accs, args[3])
        if (newkey != -1):
            print("Clave en uso.")
            exit(1)
        e.accs[position]["Clave"] = args[3]
        e.guardar()
        print("Clave cambiada con éxito.")
        exit(1)

    elif args[0] == "saldo":
        position = isIn(e.accs, args[2])
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        print("El sueldo actual es:", e.accs[position]["Saldo"])
        exit(1)

    elif args[0] == "alta":
        position = isIn(e.admacc, args[2])
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        e.accs.append({"DNI": args[3],
                       "Clave": args[4],
                       "NyA": args[5],
                       "Saldo": args[6],
                       "Hist": []})
        e.guardar()
        print("Usuario cargado con èxito.")
        exit(1)

    elif args[0] == "carga":
        position = isIn(e.admacc, args[2])
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        e.money = args[3]
        e.guardar()
        print("Saldo cargado con èxito.")
        exit(1)

    elif args[0] == "movimientos":
        position = isIn(e.admacc, args[2])
        if (position == -1):
            print("Cuenta inválida.")
            exit(1)
        userAcc = isIn(e.accs, args[3])
        if (userAcc == -1):
            print("Cuenta de usuario inexistente.")
            exit(1)
        hist = e.accs[userAcc]["Hist"]
        movs = filterHist(args[4], args[5], hist)
        print("Los movimientos realizados en esa fecha fueron:", movs)
        exit(1)

    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
