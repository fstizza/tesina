from modelos.usuario import Usuario
from constantes import dni_administrador, nombre_administrador, clave_administrador


def obtener_administrador() -> Usuario:
    usuario_administrador = Usuario()
    usuario_administrador.clave = clave_administrador
    usuario_administrador.nombre = nombre_administrador
    usuario_administrador.saldo = 0
    usuario_administrador.sueldo = 0
    usuario_administrador.dni = dni_administrador
    return usuario_administrador
