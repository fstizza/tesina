class CambioDeClaveBloqueadoError extends Error {
  constructor() {
    super('Cambio de Clave Bloqueado');
  }
}

export default CambioDeClaveBloqueadoError;
