from enum import Enum

class Op(Enum):
    EXTRACCION = 1
    CLAVE = 2

class Res(Enum):
    OK = 1
    US_INEXISTENTE = 2
    US_YA_EXISTE = 3
    CLAVE_INC = 4
    SALDO_CAJERO_INSUF = 5
    SALDO_INSUF = 6
    NO_POLITICA_EXT_1 = 7
    NO_POLITICA_EXT_2 = 8
    US_NO_HABILITADO = 9
    LIM_US_ALCANZADO = 10
    CAMBIO_CLAVE_BLOQ = 11
    NO_REQ_CLAVE_1 = 12
    NO_REQ_CLAVE_2 = 13

def interpretar_res (res):
    if (res == Res.OK):
        print("La operación se realizó correctamente.")
    elif (res == Res.US_INEXISTENTE):
        print("El DNI ingresado es inexistente.")
    elif (res == Res.US_YA_EXISTE):
        print("Ya hay un usuario con el DNI ingresado en el sistema.")
    elif (res == Res.CLAVE_INC):
        print("La clave ingresada es incorrecta.")
    elif (res == Res.SALDO_CAJERO_INSUF):
        print("El cajero no tiene saldo suficiente.")
    elif (res == Res.SALDO_INSUF):
        print("La cuenta no tiene saldo suficiente.")
    elif (res == Res.NO_POLITICA_EXT_1):
        print("La política de extracción 1 no se cumple. Alcanzó el límite diario de extracciones.")
    elif (res == Res.NO_POLITICA_EXT_2):
        print("La política de extracción 2 no se cumple. El monto es mayor a la mitad de su sueldo.")
    elif (res == Res.US_NO_HABILITADO):
        print("El DNI ingresado no corresponde a un usuario habilitado.")
    elif (res == Res.LIM_US_ALCANZADO):
        print("Se alcanzó el límite de usuarios.")
    elif (res == Res.CAMBIO_CLAVE_BLOQ):
        print("Cambio de clave bloqueado. Ya cambió la clave este mes.")
    elif (res == Res.NO_REQ_CLAVE_1):
        print("La clave ingresada no cumple el primer requisito. Es muy corta.")
    elif (res == Res.NO_REQ_CLAVE_2):
        print("La clave ingresada no cumple el segundo requisito. No es alfanumérica.")
    else:
        print("Resultado desconocido.")