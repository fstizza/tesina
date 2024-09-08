from os import sys
from estado import Estado
import time
from datetime import datetime


def extraccion(dni, clave, monto):
    estado = Estado.cargar()
    if extraccionOk(dni, clave, monto):
        estado.saldo = estado.saldo - monto
        saldoDni = int(estado.saldos.get(dni))
        estado.saldos.update({dni: saldoDni - int(monto)})
        movimientosDni = estado.movimientos.get(dni)
        movimientosDni.append([time.time(), "extraccion"])
        estado.movimientos.update({dni: movimientosDni})
        estado.guardar()
        print("La extracción se hizo correctamente.")
    else:
        extraccionError(dni, clave, monto)


def extraccionOk(dni, clave, monto):
    estado = Estado.cargar()
    movimientosDni = estado.movimientos.get(dni)
    j = 0
    now = datetime.today()
    for i in movimientosDni:
        dateI = datetime.fromtimestamp(i[0])
        if (
            dateI.year == now.year
            and dateI.month == now.month
            and dateI.day == now.day
            and i[1] == "extraccion"
        ):
            j += 1
    return (
        (dni in (estado.usuarios.keys()))
        and clave == estado.claves.get(dni)
        and monto <= estado.saldo
        and monto <= (int(estado.sueldos.get(dni)) / 2)
        and j <= 2
    )


def extraccionError(dni, clave, monto):
    if usuarioInexistente(dni):
        print("Usuario inexistente")
    elif claveIncorrecta(dni, clave):
        print("Clave incorrecta")
    elif noCumplePoliticaExtraccion(dni):
        print("Usuario no cumple política de extracción")
    elif noCumplePoliticaExtraccion2(dni, monto):
        print("Usuario no cumple política de extracción 2")
    elif saldoInsuficiente(dni, monto):
        print("Saldo insuficiente")
    elif saldoCajeroInsuficiente(monto):
        print("Saldo cajero insuficiente")


def cambioClave(dni, clave, claveNueva):
    estado = Estado.cargar()
    if cambioClaveOk(dni, clave, claveNueva):
        estado.claves.update({dni: claveNueva})
        movimientosDni = estado.movimientos.get(dni)
        movimientosDni.append([time.time(), "claves"])
        estado.movimientos.update({dni: movimientosDni})
        estado.guardar()
        print("El cambio de clave se hizo correctamente")
    else:
        cambioClaveError(dni, clave, claveNueva)


def cambioClaveOk(dni, clave, claveNueva):
    estado = Estado.cargar()
    movimientosDni = estado.movimientos.get(dni)
    j = 0
    now = datetime.today()
    for i in movimientosDni:
        dateI = datetime.fromtimestamp(i[0])
        if dateI.year == now.year and dateI.month == now.month and i[1] == "claves":
            j += 1
    return (
        (dni in (estado.usuarios.keys()))
        and clave == estado.claves.get(dni)
        and len(claveNueva) >= Estado.LONG_MIN_CLAVE
        and claveNueva.isalnum
        and j == 0
    )


def cambioClaveError(dni, clave, claveNueva):
    if usuarioInexistente(dni):
        print("Usuario inexistente")
    elif claveIncorrecta(dni, clave):
        print("Clave incorrecta")
    elif cambioDeClaveBloqueado(dni):
        print("Cambio de clave bloqueado")
    elif noCumpleRequisitosClave1(claveNueva):
        print("No cumple requisitos cambio clave 1")
    elif noCumpleRequisitosClave2(claveNueva):
        print("No cumple requisitos cambio clave 2")


def consultaSaldo(dni, clave):
    estado = Estado.cargar()
    if consultaSaldoOk(dni, clave):
        saldo = estado.saldos.get(dni)
        print("El saldo correspondiente es: " + str(saldo))
    else:
        consultaSaldoError(dni, clave)


def consultaSaldoOk(dni, clave):
    estado = Estado.cargar()
    return (dni in (estado.usuarios.keys())) and clave == estado.claves.get(dni)


def consultaSaldoError(dni, clave):
    if usuarioInexistente(dni):
        print("Usuario no habilitado")
    elif claveIncorrecta(dni, clave):
        print("Clave incorrecta")


def alta(dniAdmin, claveAdmin, dni, clave, nombre, monto):
    estado = Estado.cargar()
    if altaOk(dniAdmin, claveAdmin, dni, clave, nombre):
        estado.usuarios.update({dni: nombre})
        estado.claves.update({dni: clave})
        estado.movimientos.update({dni: []})
        estado.saldos.update({dni: monto})
        estado.sueldos.update({dni: monto})
        estado.guardar()
        print("El usuario ha sido de alta correctamente.")
    else:
        altaError(dniAdmin, claveAdmin, dni, clave, nombre)


def altaOk(dniAdmin, claveAdmin, dni, clave, nombre):
    estado = Estado.cargar()
    return (
        dniAdmin == Estado.ADMINISTRADOR
        and claveAdmin == Estado.CLAVE_ADMINISTRADOR
        and len(clave) >= Estado.LONG_MIN_CLAVE
        and not (dni in (estado.usuarios.keys()))
        and len(estado.usuarios.keys()) < Estado.CANT_MAX_USUARIOS
    )


def altaError(dniAdmin, claveAdmin, dni, clave, nombre):
    if usuarioNoHabilitado(dniAdmin):
        print("Usuario no habilitado")
    elif claveIncorrecta(dniAdmin, claveAdmin):
        print("Clave incorrecta")
    elif usuarioYaExistente(dni):
        print("Usuario ya existente")
    elif limiteUsuariosAlcanzado():
        print("Limite usuarios alcanzados")


def carga(dni, clave, monto):
    estado = Estado.cargar()
    if cargaOk(dni, clave, monto):
        estado.saldo = estado.saldo + int(monto)
        estado.guardar()
        print("La carga se hizo correctamente")
    else:
        cargaError(dni, clave, monto)


def cargaOk(dni, clave, monto):
    estado = Estado.cargar()
    return dni == Estado.ADMINISTRADOR and clave == Estado.CLAVE_ADMINISTRADOR


def cargaError(dni, clave, monto):
    if usuarioNoHabilitado(dni):
        print("Usuario no habilitado")
    elif claveIncorrecta(dni, clave):
        print("Clave incorrecta")


def consultaMovimientos(dni, clave, dniConsulta, desde, hasta):
    estado = Estado.cargar()
    if consultaMovimientosOk(dni, clave, dniConsulta, desde, hasta):
        movimientosDni = estado.movimientos.get(dniConsulta)
        movimientosFecha = []
        for i in movimientosDni:
            if i[0] > desde and i[0] < hasta:
                movimientosFecha.append(i)
        print("Los movimientos son: ")
        print(movimientosFecha)
    else:
        consultaMovimientosError(dni, clave, dniConsulta, desde, hasta)


def consultaMovimientosOk(dni, clave, dniConsulta, desde, hasta):
    estado = Estado.cargar()
    return (
        dni == Estado.ADMINISTRADOR
        and clave == Estado.CLAVE_ADMINISTRADOR
        and (dniConsulta in (estado.usuarios.keys()))
    )


def consultaMovimientosError(dni, clave, dniConsulta, desde, hasta):
    if usuarioNoHabilitado(dni):
        print("Usuario no habilitado")
    elif claveIncorrecta(dni, clave):
        print("Clave incorrecta")
    if usuarioInexistente(dniConsulta):
        print("Usuario inexistente")


# Errores


def usuarioInexistente(dni):
    estado = Estado.cargar()
    return not (dni in (estado.usuarios.keys()))


def usuarioYaExistente(dni):
    estado = Estado.cargar()
    return dni in (estado.usuarios.keys())


def claveIncorrecta(dni, clave):
    estado = Estado.cargar()
    return (dni in (estado.usuarios.keys())) and estado.claves.get(dni) != clave


def saldoCajeroInsuficiente(monto):
    estado = Estado.cargar()
    return monto > estado.saldo


def saldoInsuficiente(dni, monto):
    estado = Estado.cargar()
    return (dni in estado.saldos.keys()) and monto > int(estado.saldos.get(dni))


def noCumplePoliticaExtraccion(dni):
    estado = Estado.cargar()
    j = 0
    now = datetime.today()
    movimientosDni = estado.movimientos.get(dni)
    for i in movimientosDni:
        dateI = datetime.fromtimestamp(i[0])
        if (
            dateI.year == now.year
            and dateI.month == now.month
            and dateI.day == now.day
            and i[1] == "extraccion"
        ):
            j += 1
    return (dni in estado.movimientos.keys()) and j >= 2


def noCumplePoliticaExtraccion2(dni, monto):
    estado = Estado.cargar()
    return (dni in estado.sueldos.keys()) and monto > (int(estado.sueldos.get(dni)) / 2)


def limiteUsuariosAlcanzado():
    estado = Estado.cargar()
    return len(estado.usuarios.keys()) > Estado.CANT_MAX_USUARIOS


def cambioDeClaveBloqueado(dni):
    estado = Estado.cargar()
    movimientosDni = estado.movimientos.get(dni)
    j = 0
    now = datetime.today()
    for i in movimientosDni:
        dateI = datetime.fromtimestamp(i[0])
        if dateI.year == now.year and dateI.month == now.month and i[1] == "claves":
            j += 1
    return (dni in estado.movimientos.keys()) and j > 0


def usuarioNoHabilitado(dni):
    return dni != Estado.ADMINISTRADOR


def noCumpleRequisitosClave1(clave):
    return len(clave) < Estado.LONG_MIN_CLAVE


def noCumpleRequisitosClave2(clave):
    return not (clave.isalnum)


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        # TODO: Completar.
        extraccion(args[1], args[2], int(args[3]))
        pass
    elif args[0] == "clave":
        # TODO: Completar.
        cambioClave(args[1], args[2], args[3])
        pass
    elif args[0] == "saldo":
        # TODO: Completar.
        consultaSaldo(args[1], args[2])
        pass
    elif args[0] == "alta":
        # TODO: Completar.
        alta(args[1], args[2], args[3], args[4], args[5], args[6])
        pass
    elif args[0] == "carga":
        # TODO: Completar.
        carga(args[1], args[2], args[3])
        pass
    elif args[0] == "movimientos":
        # TODO: Completar.
        consultaMovimientos(args[1], args[2], args[3], float(args[4]), float(args[5]))
        pass
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
