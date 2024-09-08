class UsuarioInexistenteError extends Error {
  constructor() {
    super('Usuario Inexistente');
  }
}

export default UsuarioInexistenteError;
