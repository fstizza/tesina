from datetime import date
from json import JSONEncoder, dump, loads
from os.path import exists
from typing import TypedDict


class EstadoJSONEncoder(JSONEncoder):

  def default(self, o):
    if isinstance(o, date):
      return str(o)
    return super().default(o)


class Usuario(TypedDict):
  dni: str
  nombre: str
  clave: str


class Admin(Usuario):
  pass


class Cliente(Usuario):
  sueldo: float
  saldo: float


class Movimiento(TypedDict):
  dni: str
  operacion: str
  monto: float
  fecha: str


class Estado:
  """Modelo que representa el estado del sistema."""
  clientes: dict
  admins: dict
  movimientos: dict
  dinero_disponible: float

  def guardar(self):
    """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
    json = {}
    json["clientes"] = self.clientes
    json["admins"] = self.admins
    json["movimientos"] = self.movimientos
    json["dinero_disponible"] = self.dinero_disponible
    with open("estado.json", "w") as estado_archivo:
      dump(json, estado_archivo, cls=EstadoJSONEncoder)

  def cargar():
    """Retorna una instancia del modelo de estado con los valores guardados en `estado.json`."""
    contenido = ""
    if exists("estado.json"):
      with open("estado.json", "r") as estado_archivo:
        contenido = estado_archivo.read()
    if contenido != "":
      json = loads(contenido)
      estado = Estado()
      estado.clientes = json["clientes"]
      estado.admins = json["admins"]
      estado.movimientos = json["movimientos"]
      estado.dinero_disponible = json["dinero_disponible"]
      return estado
    else:
      estado = Estado.__inicial()
      return estado

  def __inicial():
    """Retorna una instancia del modelo de estado con sus valores iniciales."""
    estado = Estado()
    estado.clientes = dict()  # diccionario de la forma {nro_dni: cliente}
    estado.admins = dict()  # diccionario de la forma {nro_dni: admin}
    estado.admins['-1'] = Admin(
        dni="-1",
        nombre="admin",
        clave="admin",
    )  # agrego al admin
    estado.movimientos = dict(
    )  # diccionario de la forma {nro_dni: movimientos}
    estado.dinero_disponible = 100000.0
    estado.guardar()

    return estado


Estado.cargar = staticmethod(Estado.cargar)
""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
