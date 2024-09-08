class SaldoInsuficienteError extends Error {
  constructor() {
    super('Saldo Insuficiente');
  }
}

export default SaldoInsuficienteError;
