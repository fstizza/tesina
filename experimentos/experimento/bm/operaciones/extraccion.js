import { Estado } from '../estado.js';
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioInexistenteError from '../errores/UsuarioInexistenteError.js';
import NoCumplePoliticaExtraccionError from '../errores/NoCumplePoliticaExtraccionError.js';
import NoCumplePoliticaExtraccion2Error from '../errores/NoCumplePoliticaExtraccion2Error.js';
import SaldoInsuficienteError from '../errores/SaldoInsuficienteError.js';
import SaldoCajeroInsuficienteError from '../errores/SaldoCajeroInsuficienteError.js';
import areDatesEqual from '../utils/areDatesEqual.js';
import ParametrosInvalidosError from '../errores/ParametrosInvalidosError.js';

const extraccion = (args) => {
  const [_, dni, clave] = args;
  const monto = Number.parseFloat(args[3]);

  const estado = Estado.cargar();

  // Validaciones
  if (Number.isNaN(monto)) {
    throw new ParametrosInvalidosError();
  }

  if (!estado.usuarios[dni]) {
    throw new UsuarioInexistenteError();
  }

  if (estado.claves[dni] !== clave) {
    throw new ClaveIncorrectaError();
  }

  const movimientos = estado.movimientos[dni];
  console.log(movimientos);
  const hoy = new Date().toISOString();
  if (movimientos && movimientos.filter((movimiento) => movimiento.operacion === 'extraccion' && areDatesEqual(hoy, movimiento.fechaHora)).length > 2) {
    throw new NoCumplePoliticaExtraccionError();
  }
  console.log(movimientos.filter((movimiento) => movimiento.operacion === 'extraccion' && areDatesEqual(hoy, movimiento.fechaHora)));

  const sueldo = estado.sueldos[dni];
  if (monto > sueldo / 2) {
    throw new NoCumplePoliticaExtraccion2Error();
  }

  const saldo = estado.saldos[dni];
  if (monto > saldo) {
    throw new SaldoInsuficienteError();
  }

  if (monto > estado.saldo) {
    throw new SaldoCajeroInsuficienteError();
  }

  // Persistencia de datos
  estado.saldo -= monto;
  estado.saldos[dni] -= monto;
  estado.movimientos[dni] = [
    ...(estado.movimientos[dni] || []),
    {
      fechaHora: new Date().toISOString(),
      operacion: 'extraccion'
    },
  ];
  estado.guardar();

  return 'ok';
};

export default extraccion;