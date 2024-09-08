from json import dump, loads, JSONEncoder
from os.path import exists
from typing import TypedDict
from datetime import date


class EstadoJSONEncoder(JSONEncoder):

  def default(self, o):
    if isinstance(o, date):
      return str(o)
    return super().default(o)


class Usuario(TypedDict):
  dni: str
  nombre: str
  clave: str
  sueldo: float
  saldo: float


class Movimiento(TypedDict):
  dni: str
  operacion: str
  monto: float
  fecha: date


class Estado:
  """Modelo que representa el estado del sistema."""
  usuarios: dict
  movimientos: dict
  dinero_disponible: float

  def guardar(self):
    """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
    json = {}
    json["usuarios"] = self.usuarios
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
      estado.usuarios = json["usuarios"]
      estado.movimientos = json["movimientos"]
      estado.dinero_disponible = json["dinero_disponible"]
      return estado
    else:
      return Estado.__inicial()

  def __inicial():
    """Retorna una instancia del modelo de estado con sus valores iniciales."""
    estado = Estado()
    estado.usuarios = dict()  # diccionario de la forma {nro_dni: usuario}
    estado.usuarios['-1'] = Usuario(
      dni="-1",
      nombre="admin",
      sueldo=0.0,
      saldo=0.0,
      clave="clave_admin",
    )  # agrego al admin
    estado.movimientos = dict(
    )  # diccionario de la forma {nro_dni: movimientos}
    estado.dinero_disponible = 1000.0
    estado.guardar()

    return estado


Estado.cargar = staticmethod(Estado.cargar)
""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
