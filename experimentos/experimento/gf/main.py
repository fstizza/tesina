from os import sys

# Imports agregados
from estado import Estado
from datetime import datetime

# Constantes pedidas
CANT_MAX_USUARIOS = 5
LONG_MIN_CLAVE = 8
ahora = datetime.now()
administrador = "21354665"  # DNI
nombre_administrador = "ADMIN"
clave_administrador = "PASSW0RD"

# Constantes agregadas
FORMATO_FECHA = "%d/%m/%Y"


# Funciones externas pedidas
def LONGITUD(clave):
    return clave.length()


def DIF_FECHAS_DIAS(fecha1, fecha2):
    d1 = fecha1
    if isinstance(fecha1, str):
        d1 = datetime.strptime(fecha1, FORMATO_FECHA)
    d2 = fecha2
    if isinstance(fecha2, str):
        d2 = datetime.strptime(fecha2, FORMATO_FECHA)
    return (d1 - d2).days


def MISMO_MES(fecha1, fecha2):
    d1 = fecha1
    if isinstance(fecha1, str):
        d1 = datetime.strptime(fecha1, FORMATO_FECHA)
    d2 = fecha2
    if isinstance(fecha2, str):
        d2 = datetime.strptime(fecha2, FORMATO_FECHA)
    return (d1.month == d2.month) & (d1.year == d2.year)


def MISMO_DIA(fecha1, fecha2):
    d1 = fecha1
    if isinstance(fecha1, str):
        d1 = datetime.strptime(fecha1, FORMATO_FECHA)
    d2 = fecha2
    if isinstance(fecha2, str):
        d2 = datetime.strptime(fecha2, FORMATO_FECHA)
    return (d1.day) == (d2.day) & (d1.month) == (d2.month) & (d1.year) == (d2.year)


def CONTIENE_LETRA_NUM(string):
    return (
        str.isalnum(string)
        and (not (str.isalpha(string)))
        and (not (str.isnumeric(string)))
    )


# Happy cases
# Se omitio pasarle algunos parametros a las funciones para cosas que ya se chequean en la operacion
def ExtraccionOK(estado, dniIn, montoIn):
    estado.saldo = estado.saldo - int(montoIn)
    estado.saldos[dniIn] = estado.saldos[dniIn] - int(montoIn)
    estado.movimientos[dniIn] = estado.movimientos[dniIn] + [
        (ahora.strftime(FORMATO_FECHA), "extraccion")
    ]
    print("ok")


def ConsultaSaldoOK(estado):
    print(estado.saldo)
    print("ok")


def CambioClaveOK(estado, dniIn, newClaveIn):
    estado.claves[dniIn] = newClaveIn
    estado.movimientos[dniIn] = estado.movimientos[dniIn] + [
        (ahora.strftime(FORMATO_FECHA), "clave")
    ]
    print("ok")


def ConsultaMovimientosOK(estado, dniConsultaIn, desdeIn, hastaIn):
    fmov = [
        (f, m)
        for (f, m) in estado.movimientos[dniConsultaIn]
        if ((DIF_FECHAS_DIAS(f, desdeIn) >= 0) & (DIF_FECHAS_DIAS(hastaIn, f) >= 0))
    ]
    print(fmov)
    print("ok")


def AltaUsuarioOK(estado, dniUsIn, claveUsIn, nombreUsIn, sueldoUsIn):
    estado.movimientos[dniUsIn] = []
    estado.usuarios[dniUsIn] = nombreUsIn
    estado.claves[dniUsIn] = claveUsIn
    estado.saldos[dniUsIn] = int(sueldoUsIn)
    estado.sueldos[dniUsIn] = int(sueldoUsIn)
    print("ok")


def CargaOK(estado, saldoIn):
    estado.saldo = estado.saldo + int(saldoIn)
    print("ok")


# Errores
# Se omitio pasarle algunos parametros a las funciones para cosas que ya se chequean en la operacion
def UsuarioInexistente():
    print("usuarioInexistente")


def UsuarioYaExistente():
    print("usuarioYaExistente")


def ClaveIncorrecta():
    print("claveIncorrecta")


def SaldoCajeroInsuficiente():
    print("saldoCajeroInsuficiente")


def SaldoInsuficiente():
    print("saldoInsuficiente")


def NoCumplePoliticaExtraccion():
    print("noCumplePoliticaExtraccion")


def NoCumplePoliticaExtraccion2():
    print("noCumplePoliticaExtraccion2")


def LimiteUsuariosAlcanzado():
    print("limiteUsuariosAlcanzado")


def CambioDeClaveBloqueado():
    print("cambioDeClaveBloqueado")


def UsuarioNoHabilitado():
    print("usuarioNoHabilitado")


def NoCumpleRequisitosClave1():
    print("noCumpleRequisitosClave1")


def NoCumpleRequisitosClave2():
    print("noCumpleRequisitosClave2")


# Operaciones
# dniIn : DNI, claveIn : CLAVE, montoIn : MONTO
def Extraccion(estado, dniIn, claveIn, montoIn):
    if not (dniIn in estado.usuarios):
        UsuarioInexistente()
        exit()
    if not (estado.claves[dniIn] == claveIn):
        ClaveIncorrecta()
        exit()
    fmov = [
        (f, m)
        for (f, m) in estado.movimientos[dniIn]
        if (MISMO_DIA(f, ahora) and m == "extraccion")
    ]
    if len(fmov) > 2:
        NoCumplePoliticaExtraccion()
        exit()
    if int(montoIn) > (int(estado.sueldos[dniIn]) / 2):
        NoCumplePoliticaExtraccion2()
        exit()
    if int(montoIn) > int(estado.saldo):
        SaldoCajeroInsuficiente()
        exit()
    ExtraccionOK(estado, dniIn, montoIn)


# dniIn : DNI, claveIn : CLAVE
def ConsultaSaldo(estado, dniIn, claveIn):
    if not (dniIn in estado.usuarios):
        UsuarioInexistente()
        exit()
    if not (estado.claves[dniIn] == claveIn):
        ClaveIncorrecta()
        exit()
    ConsultaSaldoOK(estado)


# dniIn : DNI, claveIn : CLAVE, nuevaClaveIn : CLAVE
def CambioClave(estado, dniIn, claveIn, nuevaClaveIn):
    if not (dniIn in estado.usuarios):
        UsuarioInexistente()
        exit()
    if not (estado.claves[dniIn] == claveIn):
        ClaveIncorrecta()
        exit()
    cambios = [
        (f, m)
        for (f, m) in estado.movimientos[dniIn]
        if (MISMO_MES(f, ahora) and (m == "clave"))
    ]
    print(cambios)
    if len(cambios) > 0:
        CambioDeClaveBloqueado()
        exit()
    if len(nuevaClaveIn) < LONG_MIN_CLAVE:
        NoCumpleRequisitosClave1()
        exit()
    if not (CONTIENE_LETRA_NUM(nuevaClaveIn)):
        NoCumpleRequisitosClave2()
        exit()
    CambioClaveOK(estado, dniIn, nuevaClaveIn)


# dniAdminIn : DNI, claveAdminIn : CLAVE, dniUsIn : DNI, claveUsIn : CLAVE, nombreUsIn : NOMBRE, sueldoIn : MONTO
def AltaUsuario(
    estado, dniAdminIn, claveAdminIn, dniUsIn, claveUsIn, nombreUsIn, sueldoIn
):
    if not (dniAdminIn == administrador):
        UsuarioNoHabilitado()
        exit()
    if not (estado.claves[dniAdminIn] == claveAdminIn):
        ClaveIncorrecta()
        exit()
    if dniUsIn in estado.usuarios:
        UsuarioYaExistente()
        exit()
    if len(estado.usuarios) == CANT_MAX_USUARIOS:
        LimiteUsuariosAlcanzado()
        exit()
    AltaUsuarioOK(estado, dniUsIn, claveUsIn, nombreUsIn, sueldoIn)


# dniIn : DNI, claveIn : CLAVE, saldoIn : MONTO
def Carga(estado, dniIn, claveIn, saldoIn):
    if not (estado.usuarios[dniIn] == estado.usuarios[administrador]):
        UsuarioNoHabilitado()
        exit()
    if not (estado.claves[dniIn] == claveIn):
        ClaveIncorrecta()
        exit()
    CargaOK(estado, saldoIn)


# dniAdminIn : DNI, claveAdminIn : CLAVE, dniConsultaIn : DNI, desdeIn : FECHAHORA, hastaIn : FECHAHORA
def ConsultaMovimientos(
    estado, dniAdminIn, claveAdminIn, dniConsultaIn, desdeIn, hastaIn
):
    if not (dniAdminIn == administrador):
        UsuarioNoHabilitado()
        exit()
    if not (estado.claves[administrador] == claveAdminIn):
        ClaveIncorrecta()
        exit()
    if not (dniConsultaIn in estado.usuarios):
        UsuarioInexistente()
    ConsultaMovimientosOK(estado, dniConsultaIn, desdeIn, hastaIn)


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        e = Estado.cargar()
        Extraccion(e, args[1], args[2], args[3])
        e.guardar()
        pass
    elif args[0] == "clave":
        e = Estado.cargar()
        CambioClave(e, args[1], args[2], args[3])
        e.guardar()
        pass
    elif args[0] == "saldo":
        e = Estado.cargar()
        ConsultaSaldo(e, args[1], args[2])
        e.guardar()
        pass
    elif args[0] == "alta":
        e = Estado.cargar()
        AltaUsuario(e, args[1], args[2], args[3], args[4], args[5], args[6])
        e.guardar()
        pass
    elif args[0] == "carga":
        e = Estado.cargar()
        Carga(e, args[1], args[2], args[3])
        e.guardar()
        pass
    elif args[0] == "movimientos":
        e = Estado.cargar()
        ConsultaMovimientos(e, args[1], args[2], args[3], args[4], args[5])
        e.guardar()
        pass
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
