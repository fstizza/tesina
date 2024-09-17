from estado import Estado, Usuario
from operaciones.alta.parametros_alta_usuario import ParametrosAltaUsuario
from tipos import RESULTADO


def alta_usuario(solicitud: ParametrosAltaUsuario):
    estado = Estado()

    if solicitud.dni not in estado.usuarios.keys():
        return RESULTADO.UsuarioInexistente

    usuario = estado.usuarios[solicitud.dni]

    if usuario.clave != solicitud.clave:
        return RESULTADO.ClaveIncorrecta

    if solicitud.dni_usuario in estado.usuarios.keys():
        return RESULTADO.UsuarioYaExistente

    if len(estado.usuarios) >= 300:
        return RESULTADO.LimiteUsuariosAlcanzado

    nuevo_usuario = Usuario()
    nuevo_usuario.dni = solicitud.dni_usuario
    nuevo_usuario.clave = solicitud.clave_usuario
    nuevo_usuario.nombre = solicitud.nombre
    nuevo_usuario.saldo = solicitud.sueldo
    nuevo_usuario.sueldo = solicitud.sueldo

    estado.usuarios[solicitud.dni_usuario] = nuevo_usuario

    estado.guardar()

    return RESULTADO.OK
