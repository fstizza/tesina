from subops import *
from estado import Estado

def extraccion(dni, clave, monto):
    e = Estado.cargar()

    if (not usuario_existe(e, dni)):
        return Res.US_INEXISTENTE
    elif (not clave_correcta(e, dni, clave)):
        return Res.CLAVE_INC
    elif (not politica_ext_1(e, dni)):
        return Res.NO_POLITICA_EXT_1
    elif (not politica_ext_2(e, dni, monto)):
        return Res.NO_POLITICA_EXT_2
    elif (not saldo_suficiente(e, dni, monto)):
        return Res.SALDO_INSUF
    elif (not saldo_cajero_suficiente(e, monto)):
        return Res.SALDO_CAJERO_INSUF
    else:
        extraccion_ok(e, dni, monto)
        e.guardar()
        return Res.OK

def cambio_clave(dni, clave, nueva_clave):
    e = Estado.cargar()

    if (not usuario_existe(e, dni)):
        return Res.US_INEXISTENTE
    elif (not clave_correcta(e, dni, clave)):
        return Res.CLAVE_INC
    elif (cambio_clave_bloq(e, dni)):
        return Res.CAMBIO_CLAVE_BLOQ
    elif (not req_clave_1(e, nueva_clave)):
        return Res.NO_REQ_CLAVE_1
    elif (not req_clave_2(e, nueva_clave)):
        return Res.NO_REQ_CLAVE_2
    else:
        cambio_clave_ok (e, dni, nueva_clave)
        e.guardar()
        return Res.OK

def consulta_saldo(dni, clave):
    e = Estado.cargar()

    if (not usuario_existe(e, dni)):
        return (Res.US_INEXISTENTE,0)
    elif (not clave_correcta(e, dni, clave)):
        return (Res.CLAVE_INC,0)
    else:
        saldo = consulta_saldo_ok(e, dni)
        return (Res.OK,saldo)

def alta_usuario(dni_admin, clave_admin, dni, clave, nombre, sueldo):
    e = Estado.cargar()

    if (not usuario_habilitado(e, dni_admin)):
        return Res.US_NO_HABILITADO
    elif (not clave_correcta(e, dni_admin, clave_admin)):
        return Res.CLAVE_INC
    elif (usuario_existe(e, dni)):
        return Res.US_YA_EXISTE
    elif (lim_alcanzado(e)):
        return Res.LIM_US_ALCANZADO
    else:
        alta_usuario_ok(e, dni, clave, nombre, sueldo)
        e.guardar()
        return Res.OK

def carga(dni, clave, saldo):
    e = Estado.cargar()

    if (not usuario_habilitado(e, dni)):
        return Res.US_NO_HABILITADO
    elif (not clave_correcta(e, dni, clave)):
        return Res.CLAVE_INC
    else:
        carga_ok(e, saldo)
        e.guardar()
        return Res.OK

def consulta_movimientos(dni, clave, dni_c, desde, hasta):
    e = Estado.cargar()

    if (not usuario_habilitado(e, dni)):
        return (Res.US_NO_HABILITADO,[])
    elif (not usuario_existe(e, dni_c)):
        return (Res.US_INEXISTENTE,[])
    elif (not clave_correcta(e, dni, clave)):
        return (Res.CLAVE_INC,[])
    else:
        mov = consulta_movimientos_ok(e, dni_c, desde, hasta)
        return (Res.OK,mov)

