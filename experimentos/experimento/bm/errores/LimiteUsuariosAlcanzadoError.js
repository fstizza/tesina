class LimiteUsuariosAlcanzadoError extends Error {
  constructor() {
    super('Limite Usuarios Alcanzado');
  }
}

export default LimiteUsuariosAlcanzadoError;
