class SaldoCajeroInsuficienteError extends Error {
  constructor() {
    super('Saldo Cajero Insuficiente');
  }
}

export default SaldoCajeroInsuficienteError;
