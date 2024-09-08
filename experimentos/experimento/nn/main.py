from json import dump, dumps
from abst_types import DNI, NOMBRE, CLAVE, FECHAHORA
from syn_types import MONTO
from estado import Estado
from enums import RESULTADO, OPERACION
from ext_func import subconj_movimientos_ventana, longitud, subconj_movimientos_mismo_dia, subconj_movimientos_mismo_mes

from os import sys
from datetime import datetime


def usuarioInexistente(dni: DNI, estado: Estado) -> RESULTADO:
    if estado.usuarios.get(dni) == None:
        return RESULTADO.usuarioInexistente
    return None


def usuarioYaExiste(dni: DNI, estado: Estado) -> RESULTADO:
    if estado.usuarios.get(dni) != None:
        return RESULTADO.usuarioYaExistente
    return None


def claveIncorrecta(dni: DNI, clave: CLAVE, estado: Estado) -> RESULTADO:
    user = estado.usuarios.get(dni)
    clave_real = estado.claves.get(dni)
    if clave != clave_real:
        return RESULTADO.claveIncorrecta
    return None


def saldoCajeroInsuficiente(monto: MONTO, estado: Estado) -> RESULTADO:
    if monto > int(estado.saldo):
        return RESULTADO.saldoCajeroInsuficiente
    return None


def saldoInsuficiente(dni: DNI, monto: MONTO, estado: Estado) -> RESULTADO:
    user = estado.usuarios.get(dni)
    if monto > int(estado.saldos.get(dni)):
        return RESULTADO.saldoInsuficiente
    return None


def noCumplePoliticaExtraccion(dni: DNI, estado: Estado) -> RESULTADO:
    movimientos = estado.movimientos.get(dni)
    # if movimientos != None return RESULTADO.noCumplePoliticaExtraccion
    movimientos = [m for m in movimientos if m[1] == OPERACION.extraccion.name]
    n_extracciones_hoy = len(
        subconj_movimientos_mismo_dia(Estado.AHORA, movimientos))
    if n_extracciones_hoy > 2:
        return RESULTADO.noCumplePoliticaExtraccion
    return None


def noCumplePoliticaExtraccion2(dni: DNI, monto: MONTO, estado: Estado) -> RESULTADO:
    sueldo = float(estado.sueldos.get(dni))
    # if sueldo != None return true
    if monto > sueldo / 2:
        return RESULTADO.noCumplePoliticaExtraccion2
    return None


def limiteUsuariosAlcanzado(estado: Estado) -> RESULTADO:
    if len(estado.usuarios) >= estado.CANT_MAX_USUARIOS:
        return RESULTADO.limiteUsuariosAlcanzado
    return None


def cambioDeClaveBloqueado(dni: DNI, estado: Estado) -> RESULTADO:
    movimientos = estado.movimientos.get(dni)
    # if movimientos != None return true
    movimientos = [m for m in movimientos if m[1] == OPERACION.clave.name]
    cambio_de_clave_mes = subconj_movimientos_mismo_mes(
        Estado.AHORA, movimientos)
    if cambio_de_clave_mes != set():
        return RESULTADO.cambioDeClaveBloqueado
    return None


def usuarioNoHabilitado(dni: DNI, estado: Estado) -> RESULTADO:
    if dni != estado.ADMINISTRADOR:
        return RESULTADO.usuarioNoHabilitado
    return None


def noCumpleRequisitosClave1(clave: CLAVE, estado: Estado) -> RESULTADO:
    if len(clave) < estado.LONG_MIN_CLAVE:
        return RESULTADO.noCumpleRequisitosClave1
    return None


def noCumpleRequisitosClave2(clave: str, estado: Estado) -> RESULTADO:
    try:
        CLAVE(clave)
    except ValueError:
        return RESULTADO.noCumpleRequisitosClave2
    return None


def consultaSaldoOk(dni: DNI, clave: CLAVE, estado: Estado) -> MONTO:
    # dni in dom usr
    # clave_real = estado.claves.get(dni)

    return RESULTADO.ok, estado.saldos[dni]


def consultaSaldo(dni: DNI, clave: CLAVE, estado: Estado):
    if usuarioInexistente(dni, estado):
        return usuarioInexistente(dni, estado)
    if claveIncorrecta(dni, clave, estado):
        return claveIncorrecta(dni, clave, estado)

    return consultaSaldoOk(dni, clave, estado)


def extraccionOk(dni: DNI, clave: CLAVE, monto: MONTO, estado: Estado):
    # dni in dom usr
    # clave_real = estado.claves.get(dni)
    # chequedo extraccion dia (politica extraccion 1)
    # cumple politica extraccion 2
    # el cajero tiene saldo suficiente
    estado.saldo = str(int(estado.saldo) - monto)
    estado.saldos[dni] = str(int(estado.saldos[dni]) - monto)

    new_dni_mov = [(datetime.now(), OPERACION.extraccion.name)]
    estado.movimientos[dni] = estado.movimientos[dni].union(set(new_dni_mov))

    return RESULTADO.ok


def extraccion(dni: DNI, clave: CLAVE, monto: MONTO, estado: Estado):
    if usuarioInexistente(dni, estado):
        return usuarioInexistente(dni, estado)
    if claveIncorrecta(dni, clave, estado):
        return claveIncorrecta(dni, clave, estado)
    if noCumplePoliticaExtraccion(dni, estado):
        return noCumplePoliticaExtraccion(dni, estado)
    if noCumplePoliticaExtraccion2(dni, monto, estado):
        return noCumplePoliticaExtraccion2(dni, monto, estado)
    if saldoInsuficiente(dni, monto, estado):
        return saldoInsuficiente(dni, monto, estado)
    if saldoCajeroInsuficiente(monto, estado):
        return saldoCajeroInsuficiente(monto, estado)

    return extraccionOk(dni, clave, monto, estado)


def cambioDeClaveOk(dni: DNI, clave: CLAVE, nueva_clave: CLAVE, estado: Estado):
    # dni in dom usr
    # clave_real = estado.claves.get(dni)
    # cumpleRequisitosClave1
    # cumpleRequisitosClave2
    # cambio de clave no bloqueado
    estado.claves[dni] = nueva_clave

    new_dni_mov = [(datetime.now(), OPERACION.clave.name)]
    estado.movimientos[dni] = estado.movimientos[dni].union(set(new_dni_mov))

    return RESULTADO.ok


def cambioDeClave(dni: DNI, clave: str, nueva_clave: str, estado: Estado):
    if noCumpleRequisitosClave2(nueva_clave, estado):
        return noCumpleRequisitosClave2(nueva_clave, estado)
    if usuarioInexistente(dni, estado):
        return usuarioInexistente(dni, estado)
    if claveIncorrecta(dni, clave, estado):
        return claveIncorrecta(dni, clave, estado)
    if cambioDeClaveBloqueado(dni, estado):
        return cambioDeClaveBloqueado(dni, estado)
    if noCumpleRequisitosClave1(nueva_clave, estado):
        return noCumpleRequisitosClave1(nueva_clave, estado)

    return cambioDeClaveOk(dni, clave, nueva_clave, estado)


def consultaMovimientosOk(dni: DNI, clave: CLAVE, dni_consulta: DNI, desde: FECHAHORA, hasta: FECHAHORA, estado: Estado):
    # usuario es admin
    # clave ok
    # dni_consulta in dom usr
    user_movimientos = estado.movimientos[dni_consulta]
    movimientos = subconj_movimientos_ventana(desde, hasta, user_movimientos)

    return RESULTADO.ok, movimientos


def consultaMovimientos(dni: DNI, clave: CLAVE, dni_consulta: DNI, desde: FECHAHORA, hasta: FECHAHORA, estado: Estado):
    if usuarioNoHabilitado(dni, estado):
        return usuarioNoHabilitado(dni, estado)
    if claveIncorrecta(dni, clave, estado):
        return claveIncorrecta(dni, clave, estado)
    if usuarioInexistente(dni_consulta, estado):
        return usuarioInexistente(dni_consulta, estado)

    return consultaMovimientosOk(dni, clave, dni_consulta, desde, hasta, estado)


def altaUsuarioOk(dni: DNI, clave: CLAVE, dni_usuario: DNI, clave_usuario: CLAVE, nombre: NOMBRE, sueldo: MONTO, estado: Estado):
    # usuario es admin
    # clave ok
    # dni nuevo no exista
    # no se haya alcanzado el limite de usuarios
    estado.movimientos[dni_usuario] = set()
    estado.usuarios[dni_usuario] = nombre
    estado.claves[dni_usuario] = clave_usuario
    estado.saldos[dni_usuario] = sueldo
    estado.sueldos[dni_usuario] = sueldo

    return RESULTADO.ok


def altaUsuario(dni: DNI, clave: CLAVE, dni_usuario: DNI, clave_usuario: CLAVE, nombre: NOMBRE, sueldo: MONTO, estado: Estado):
    if usuarioNoHabilitado(dni, estado):
        return usuarioNoHabilitado(dni, estado)
    if claveIncorrecta(dni, clave, estado):
        return claveIncorrecta(dni, clave, estado)
    if usuarioYaExiste(dni_usuario, estado):
        return usuarioYaExiste(dni_usuario, estado)
    if limiteUsuariosAlcanzado(estado):
        return limiteUsuariosAlcanzado(estado)

    return altaUsuarioOk(dni, clave, dni_usuario, clave_usuario, nombre, sueldo, estado)


def cargaOK(dni_admin: DNI, clave_admin: CLAVE, saldo: MONTO, estado: Estado):
    # check admin
    # check clave
    estado.saldo += saldo

    return RESULTADO.ok


def carga(dni_admin: DNI, clave_admin: CLAVE, saldo: MONTO, estado: Estado):
    if usuarioNoHabilitado(dni_admin, estado):
        return usuarioNoHabilitado(dni_admin, estado)
    if claveIncorrecta(dni_admin, clave_admin, estado):
        return claveIncorrecta(dni_admin, clave_admin, estado)

    return cargaOK(dni_admin, clave_admin, saldo, estado)


def esMontoNatural(monto: int) -> bool:
    return monto >= 0


def main(args: list):

    estado = Estado.cargar()
    estado.guardar()
    # test = consultaSaldo("usr_test", "clave_test", 42, estado)
    # print(test)

    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)

    if args[0] == "extraccion":
        dni = args[1]
        clave = args[2]
        monto = int(args[3])

        if not esMontoNatural(monto):
            print("El valor de monto ingresado no es un numero natural.")
            return

        print(extraccion(dni, clave, monto, estado))

    elif args[0] == "clave":
        dni = args[1]
        clave = args[2]
        nueva_clave = args[3]

        print(cambioDeClave(dni, clave, nueva_clave, estado))

    elif args[0] == "saldo":
        dni = args[1]
        clave = args[2]

        print(consultaSaldo(dni, clave, estado))

    elif args[0] == "alta":
        dni = args[1]
        clave = args[2]
        dni_usuario = args[3]
        clave_usuario = args[4]
        nombre = args[5]
        sueldo = int(args[6])

        if not esMontoNatural(sueldo):
            print("El valor de sueldo ingresado no es un numero natural.")
            return

        print(altaUsuario(dni, clave, dni_usuario,
              clave_usuario, nombre, sueldo, estado))

    elif args[0] == "carga":
        dni_admin = args[1]
        clave_admin = args[2]
        saldo = int(args[3])

        print(carga(dni_admin, clave_admin, saldo, estado))

    elif args[0] == "movimientos":
        dni = args[1]
        clave = args[2]
        dni_consulta = args[3]
        desde = datetime.strptime(args[4], '%Y-%m-%d')
        hasta = datetime.strptime(args[5], '%Y-%m-%d')

        res = consultaMovimientos(
            dni, clave, dni_consulta, desde, hasta, estado)
        if (len(res) == 2):
            print(
                dumps(
                list(
                    map(
                        lambda m: {
                            'fechaHora': datetime.strftime(m[0], '%Y-%m-%d'),
                            'operacion': m[1]
                        },
                        list(res[1])
                    ))))
        else:
            print(res)

    else:
        print("Operación inválida.")
        exit(1)

    estado.guardar()


if __name__ == "__main__":
    main(sys.argv[1:])
