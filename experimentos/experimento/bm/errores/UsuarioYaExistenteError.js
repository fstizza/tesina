class UsuarioYaExistenteError extends Error {
  constructor() {
    super('Usuario Ya Existente');
  }
}

export default UsuarioYaExistenteError;
