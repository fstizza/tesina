import re
from datetime import datetime

from os import sys
from datetime import date

from estado import Admin, Cliente, Estado, Movimiento, Usuario


def validarArgumentos(args: list, cant: int):
  '''
  Corroborar que el numero de argumentos es el indicado

  args: lista de argumentos
  cant: cantidad de argumentos que se espera
  '''
  if (len(args) != cant):
    print("Error: Numero de argumentos invalido")
    exit(1)


def validarCarga(disponible, monto):
  '''
  Validar el monto resultante no sea negativo

  disponible: monto disponible
  monto: monto a cargar
  '''
  if disponible + monto < 0:
    print("Error: Monto invalido")
    exit(1)


def validarClave(clave: str):
  '''
  Validar que la clave sea alfanumerica y de al meenos
  8 caracteres

  clave: clave a validar
  '''
  if len(clave) < 8:
    print("Error: La clave debe contener al menos 8 caracteres")
    exit(1)

  if not clave.isalnum():
    print("Error: La clave debe contener solo caracteres alfanumericos")
    exit(1)


def validarFechaCambioClave(movimientos_usuario: dict, mes_actual: str):
  existe_cambio_de_clave = any([
      movimiento for movimiento in movimientos_usuario
      if movimiento.get("fecha").split('/')[1] == mes_actual
      and movimiento.get("operacion") == "clave"
  ])
  if existe_cambio_de_clave:
    print("Ya se realizo un cambio de clave este mes.")
    exit(1)


def esClaveDeUsuario(usuario: Usuario, clave: str):
  '''
  Corroborar que la clave corresponde al usuario

  usuario: usuario a corroborar
  clave: clave a corroborar
  '''
  return usuario['clave'] == clave


def validarFechas(desde: str, hasta: str):
  '''
  Corroborar que el formato y el intervalo de las
  fechas es valido

  desde: fecha inicial
  hasta: fecha final
  '''
  try:
    d_desde = datetime.strptime(desde, "%d/%m/%Y")
    d_hasta = datetime.strptime(hasta, "%d/%m/%Y")
  except:
    print("Formato de fecha invalido, debe ser de la forma dd/mm/yyyy")
    exit(1)
  if (d_desde > d_hasta):
    print("Error: Fechas invalidas, desde debe ser menor a hasta")
    exit(1)


def usuarioExistente(usuarios: dict, dni: str):
  '''
  Corroborar que el usuario existe

  usuario: usuario a corroborar
  dni: identificador de usuario
  '''
  return dni in usuarios


def validarUsuario(usuarios: dict, dni: str, clave: str):
  '''
  Corroborar que el usuario es un usuario valido
  '''
  existe = usuarioExistente(usuarios, dni)
  if not existe:
    return existe
  clave_valida = esClaveDeUsuario(usuarios[dni], clave)
  return clave_valida


def validarCliente(usuarios: dict, dni: str, clave: str):
  if (not validarUsuario(usuarios, dni, clave)):
    print("Error: Cliente inexistente o clave incorrecta")
    exit(1)


def validarAdmin(admins: dict, dni: str, clave: str):
  if (not validarUsuario(admins, dni, clave)):
    print("Error: Admin inexistente o clave incorrecta")
    exit(1)


def validarExtraccion(disponible: float, cliente: Cliente, monto: float):
  '''
  Validar que el monto no sea negativo, el saldo sea suficiente
  y haya suficiente dinero en el cajero.
  '''
  if monto <= 0:
    print("Error: Monto invalido")
    exit(1)
  if disponible < monto:
    print("Error: Monto no disponible")
    exit(1)
  if cliente.get('saldo') / 2 < monto:
    print("Error: Saldo insuficiente")
    exit(1)


def validarCantExtracciones(movimientos: dict, dni: str):
  hoy = date.today().strftime('%d/%m/%Y')
  movimientos_usuario = movimientos.get(dni, [])
  cant_extracciones = len([
      movimiento for movimiento in movimientos_usuario
      if movimiento.get("fecha") == hoy
      and movimiento.get("operacion") == "extraccion"
  ])
  if cant_extracciones >= 3:
    print("Se realizo el maximo de extracciones por hoy.")
    exit(1)


def obtenerCliente(usuarios: dict, dni: str, clave: str) -> Cliente:
  validarCliente(usuarios, dni, clave)
  return usuarios[dni]


def main(args: list):
  if len(args) == 0:
    print("Sin argumentos.")
    exit(1)

  est = Estado.cargar()

  if args[0] == "extraccion":
    validarArgumentos(args[1:], 3)
    dni, clave, monto = args[1:]
    cli = obtenerCliente(est.clientes, dni, clave)

    # Corrobor validez operacion
    validarExtraccion(est.dinero_disponible, cli, float(monto))
    validarCantExtracciones(est.movimientos, dni)

    # actualizo el saldo del usuario
    cli["saldo"] = cli["saldo"] - float(monto)
    est.clientes[dni] = cli
    movimientos_usuario = est.movimientos.get(dni, [])
    movimientos_usuario.append(
        Movimiento(dni=dni,
                   operacion='extraccion',
                   monto=float(monto),
                   fecha=date.today().strftime('%d/%m/%Y')))
    est.movimientos[dni] = movimientos_usuario
    est.dinero_disponible -= float(monto)
    est.guardar()

    print("Saldo extraido con exito.")

    est.guardar()

  elif args[0] == "clave":
    validarArgumentos(args[1:], 3)
    dni, actual, nueva = args[1:]
    cliente = obtenerCliente(est.clientes, dni, actual)

    # validacion cambio de clave
    mes_actual = str(date.today().month)
    movimientos_usuario = est.movimientos.get(dni, [])
    validarFechaCambioClave(movimientos_usuario, mes_actual)
    validarClave(nueva)

    #cambio de clave
    cliente["clave"] = nueva
    hoy: str = date.today().strftime('%d/%m/%Y')
    movimientos_usuario.append(
        Movimiento(dni=dni, operacion='clave', fecha=hoy))
    est.movimientos[dni] = movimientos_usuario
    est.clientes[dni] = cliente
    est.guardar()
    print("Clave actualizada de forma correcta")

  elif args[0] == "saldo":
    validarArgumentos(args[1:], 2)
    dni, clave = args[1:]
    cli: Cliente = obtenerCliente(est.clientes, dni, clave)
    print("El saldo actual es de: ", cli.get('saldo'))

  elif args[0] == "alta":
    validarArgumentos(args[1:], 7)
    dni_administrador, clave_administrador = args[1:3]
    dni, clave, nombre, sueldo, saldo = args[3:]

    # Corroborar que la operacion es posible
    validarAdmin(est.admins, dni_administrador, clave_administrador)
    if (len(est.clientes) >= 5):
      print("Se alcanzo el limite de usuarios")
    if (usuarioExistente(est.clientes, dni)):
      print("El usuario ya existe")
      exit(1)
    if (saldo != sueldo):
      print("El saldo inicial debe ser igual al sueldo mensual declarado.")
      exit(1)

    #Agrego el nuevo cliente
    nuevo_usuario = Cliente(dni=dni,
                            nombre=nombre,
                            sueldo=float(sueldo),
                            saldo=float(saldo),
                            clave=clave)

    est.clientes[dni] = nuevo_usuario

    est.guardar()
    print("Usuario creado con exito.")

  elif args[0] == "carga":
    validarArgumentos(args[1:], 3)
    dni, clave, monto = args[1:]
    validarAdmin(est.admins, dni, clave)
    validarCarga(est.dinero_disponible, float(monto))
    est.dinero_disponible += float(monto)
    est.guardar()
    print("Carga exitosa")

  elif args[0] == "movimientos":
    validarArgumentos(args[1:], 5)
    dni_administrador, clave_administrador, dni_consulta, desde, hasta = args[
        1:]
    validarFechas(desde, hasta)
    validarAdmin(est.admins, dni_administrador, clave_administrador)
    existe = usuarioExistente(est.clientes, dni_consulta)

    if (not existe):
      print("Error: Cliente inexistente")
      exit(1)
    movimientos_usuario = [
        m for m in est.movimientos.get(dni_consulta, [])
        if desde <= m['fecha'] <= hasta
    ]

    print(
        "Los movimientos del usuario dentro del rango de fechas indicado, son los siguientes: "
    )
    for m in movimientos_usuario:
      print(
          f"Operacion: {m['operacion']}, Fecha: {m['fecha']}, Monto: {m.get('monto', '-')}"
      )
  else:
    print("Operación inválida.")
    exit(1)


if __name__ == "__main__":
  main(sys.argv[1:])

# Pruebas #
# python3 main.py alta -1 admin 1 clave_user1 user1 20 20
# python3 main.py alta -1 admin 1 claveuser2 user2 5000 5000

# python3 main.py extraccion 2 claveuser2 6000

# python3 main.py extraccion 1 clave_user1 3
# python3 main.py saldo 1 clave_user1
# python3 main.py extraccion 1 clave_user1 3
# python3 main.py saldo 1 clave_user1
# python3 main.py extraccion 1 clave_user1 3
# python3 main.py saldo 1 clave_user1
# python3 main.py extraccion 1 clave_user1 3

# python3 main.py clave 1 clave_user1 nueva_clave_user1
# python3 main.py clave 1 clave_user1 claveuser1
# python3 main.py carga -1 admin 100

# python3 main.py movimientos -1 admin 1 01/09/2023 10/11/2023
# Los movimientos del usuario dentro del rango de fechas indicado, son los siguientes:
# Operacion: extraccion, Fecha: 05/11/2023, Monto: 3.0
# Operacion: extraccion, Fecha: 05/11/2023, Monto: 3.0
# Operacion: extraccion, Fecha: 05/11/2023, Monto: 3.0
# Operacion: clave, Fecha: 2023-10-04, Monto: -
