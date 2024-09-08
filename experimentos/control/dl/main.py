import re

from os import sys
from datetime import date

from estado import Estado, Usuario, Movimiento


def obtener_usuario(estado: Estado, dni: str) -> Usuario:
  usuario: Usuario = estado.usuarios.get(dni)
  if not usuario:
    print("Usuario no existe.")
    exit(1)
  return usuario


def validar_clave(usuario: Usuario, clave):
  if usuario.get("clave") != clave:
    print("Clave incorrecta.")
    exit(1)


def main(args: list):
  if len(args) == 0:
    print("Sin argumentos.")
    exit(1)

  e = Estado.cargar()

  if args[0] == "extraccion":
    if len(args[1:]) != 3:
      print("Numero de argumentos erroneo.")
      exit(1)

    dni, clave, monto = args[1:]
    usuario: Usuario = obtener_usuario(estado=e, dni=dni)
    validar_clave(usuario, clave)

    # validar que el monto de la extraccion no supere la mitad de su sueldo
    if usuario.get("saldo") / 2 < float(monto):
      print("El monto de la extraccion no debe superar la mitad de su sueldo.")
      exit(1)
    # validar que el monto sea menor al monto disponible del cajero
    if e.dinero_disponible < float(monto):
      print("Monto no disponible.")
      exit(1)

    # validar cantidad de extracciones
    hoy = str(date.today())
    movimientos_usuario = e.movimientos.get(dni, [])
    cant_extracciones = len([
      movimiento for movimiento in movimientos_usuario
      if movimiento.get("fecha") == hoy
      and movimiento.get("operacion") == "extraccion"
    ])
    if cant_extracciones >= 3:
      print("Maximo de extracciones realizado por hoy.")
      exit(1)

    # actualizo el saldo del usuario
    usuario["saldo"] = usuario["saldo"] - float(monto)
    e.usuarios[dni] = usuario

    movimientos_usuario.append(
      Movimiento(dni=dni,
                 operacion='extraccion',
                 monto=float(monto),
                 fecha=date.today()))
    e.movimientos[dni] = movimientos_usuario
    e.dinero_disponible -= float(monto)
    e.guardar()

    print("Saldo extraido con exito.")
  elif args[0] == "clave":
    if len(args[1:]) != 3:
      print("Numero de argumentos erroneo.")
      exit(1)

    dni, actual, nueva = args[1:]
    usuario = obtener_usuario(estado=e, dni=dni)
    validar_clave(usuario, actual)

    # validacion nueva clave
    patron = r'^[a-zA-Z0-9]+$'

    if len(nueva) < 8:
      print("Clave muy corta.")
      exit(1)
    if not re.match(patron, nueva):
      print("Clave debe ser una combinacion de letras y numeros.")
      exit(1)

    # validacion fecha de cambio de clave
    mes_actual = str(date.today().month)
    movimientos_usuario = e.movimientos.get(dni, [])
    existe_cambio_de_clave = any([
      movimiento for movimiento in movimientos_usuario
      if movimiento.get("fecha").split('-')[1] == mes_actual
      and movimiento.get("operacion") == "clave"
    ])
    if existe_cambio_de_clave:
      print("Ya se realizo un cambio de clave este mes.")
      exit(1)

    # actualizo la clave
    usuario["clave"] = nueva
    movimientos_usuario.append(
      Movimiento(dni=dni, operacion='clave', fecha=date.today()))
    e.movimientos[dni] = movimientos_usuario
    e.guardar()

    print("La clave fue actualizada correctamente.")
  elif args[0] == "saldo":
    if len(args[1:]) != 2:
      print("Numero de argumentos erroneo.")
      exit(1)
    dni, clave = args[1:]

    usuario = obtener_usuario(estado=e, dni=dni)
    validar_clave(usuario, clave)

    print(f"El saldo del usuario {dni} es de {usuario.get('saldo')}")
  elif args[0] == "alta":
    if len(args[1:]) != 7:
      print("Numero de argumentos erroneo.")
      exit(1)
    dni_administrador, clave_administrador, dni, clave, nombre, sueldo, saldo = args[
      1:]
    administrador = obtener_usuario(estado=e, dni=dni_administrador)
    validar_clave(usuario=administrador, clave=clave_administrador)

    # valido si el usuario ya existe
    if e.usuarios.get(dni):
      print("El usuario ya existe.")
      exit(1)

    # valido la cantidad de usuarios en el sistema
    if len(e.usuarios) >= 5:
      print("No se puede agregar el usuario: Maxima capacidad de usuarios.")
      exit(1)

    # valido saldo inicial con sueldo mensual
    if sueldo != saldo:
      print("El saldo inicial debe ser igual al sueldo mensual declarado.")
      exit(1)

    nuevo_usuario = Usuario(dni=dni,
                            nombre=nombre,
                            sueldo=float(sueldo),
                            saldo=float(saldo),
                            clave=clave)
    e.usuarios[dni] = nuevo_usuario

    e.guardar()

    print("Usuario creado exitosamente.")
  elif args[0] == "carga":
    if len(args[1:]) != 3:
      print("Numero de argumentos erroneo.")
      exit(1)
    dni_administrador, clave_administrador, monto = args[1:]

    administrador = obtener_usuario(estado=e, dni=dni_administrador)
    validar_clave(usuario=administrador, clave=clave_administrador)

    e.dinero_disponible += float(monto)
    e.guardar()

    print("La carga se realizo exitosamente.")
  elif args[0] == "movimientos":
    if len(args[1:]) != 5:
      print("Numero de argumentos erroneo.")
      exit(1)
    dni_administrador, clave_administrador, dni_consulta, desde, hasta = args[
      1:]

    if desde > hasta:
      print("La fecha inicial debe menor que la final.")
      exit(1)

    administrador = obtener_usuario(estado=e, dni=dni_administrador)
    validar_clave(usuario=administrador, clave=clave_administrador)

    movimientos_usuario = [
      m for m in e.movimientos.get(dni_consulta, [])
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
# python3 main.py alta -1 clave_admin 1 clave_user1 user1 20 20
# python3 main.py alta -1 clave_admin 1 claveuser2 user2 5000 5000

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
# python3 main.py carga -1 clave_admin 100

# python3 main.py movimientos -1 clave_admin 1 2023-09-01 2023-11-10
# Los movimientos del usuario dentro del rango de fechas indicado, son los siguientes:
# Operacion: extraccion, Fecha: 2023-10-04, Monto: 3.0
# Operacion: extraccion, Fecha: 2023-10-04, Monto: 3.0
# Operacion: extraccion, Fecha: 2023-10-04, Monto: 3.0
# Operacion: clave, Fecha: 2023-10-04, Monto: -
