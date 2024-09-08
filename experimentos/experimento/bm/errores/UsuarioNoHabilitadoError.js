class UsuarioNoHabilitadoError extends Error {
  constructor() {
    super('Usuario No Habilitado');
  }
}

export default UsuarioNoHabilitadoError;
