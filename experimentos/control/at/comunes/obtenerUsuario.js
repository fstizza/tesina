// retorna el usuario si encuentra el usuario del estado que ya posee el dni, false caso contrario.
export function obtenerUsuario(e, dni) {
  let usuarios = e.usuarios
  let usuario = usuarios.find((usuario) => {
    return usuario.dni === dni;
  })
  if (usuario === undefined) return false
  return usuario
}