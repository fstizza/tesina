from estado import Estado
from enums import *
from tiempo import *

## CONDICIONES: funciones que evalúan las diferentes condiciones de las operaciones

def usuario_existe (estado, dni):
    return (dni in estado.usuarios.keys())

def clave_correcta (estado, dni, clave):
    claves = estado.claves
    return (dni in claves.keys() and claves[dni] == clave)

def saldo_cajero_suficiente (estado, monto):
    return (monto < estado.saldo)

def saldo_suficiente (estado, dni, monto):
    saldos = estado.saldos
    return (dni in saldos.keys() and monto < saldos[dni])

def politica_ext_1 (estado, dni):
    if (dni in estado.movimientos.keys()):
        extr = [(fecha,op) for (fecha,op) in estado.movimientos[dni] \
                           if op == Op.EXTRACCION and mismo_dia(ahora(),fecha)]
        return (len(extr) <= 2)
    return False

def politica_ext_2 (estado, dni, monto):
    if (dni in estado.sueldos.keys()):
        return (monto <= estado.sueldos[dni] // 2)
    return False

def lim_alcanzado (estado):
    return (len(estado.usuarios.keys()) >= estado.CANT_MAX_USUARIOS)

def cambio_clave_bloq (estado, dni):
    if (dni in estado.movimientos.keys()):
        cambios = [(fecha,op) for (fecha,op) in estado.movimientos[dni] \
                              if op == Op.CLAVE and mismo_mes(ahora(),fecha)]
        return (cambios != [])
    return True

def usuario_habilitado (estado, dni):
    return (dni == estado.DNI_ADMIN)

def req_clave_1 (estado, clave):
    return (len(clave) >= estado.LONG_MIN_CLAVE)

def req_clave_2 (estado, clave):
    return (clave.isalnum())

## OPERACIONES OK: funciones que ejecutan las operaciones correctas

def consulta_saldo_ok (estado, dni):
    return (estado.saldos[dni])

def extraccion_ok (estado, dni, monto):
    estado.saldo -= monto
    estado.saldos[dni] -= monto
    estado.movimientos[dni].append((ahora(),Op.EXTRACCION))

def cambio_clave_ok (estado, dni, nueva_clave):
    estado.claves[dni] = nueva_clave
    estado.movimientos[dni].append((ahora(),Op.CLAVE))

def consulta_movimientos_ok (estado, dni, desde, hasta):
    mov = [(fecha,op) for (fecha,op) in estado.movimientos[dni] \
                      if dif_fechas_dias(fecha,desde) >= 0 and dif_fechas_dias(hasta,fecha) >= 0]
    return mov

def alta_usuario_ok (estado, dni, clave, nombre, sueldo):
    estado.movimientos[dni] = [] 
    estado.usuarios[dni] = nombre
    estado.claves[dni] = clave
    estado.saldos[dni] = sueldo
    estado.sueldos[dni] = sueldo

def carga_ok (estado, saldo):
    estado.saldo += saldo



