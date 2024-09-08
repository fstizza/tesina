import { Estado } from "../estado.js";
import ParametrosInvalidosError from '../errores/ParametrosInvalidosError.js';
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioNoHabilitadoError from '../errores/UsuarioNoHabilitadoError.js';

const carga = (args) => {
  const [_, dniAdmin, claveAdmin] = args;
  const saldo = Number.parseFloat(args[3]);

  const estado = Estado.cargar();

  // Validaciones
  if (Number.isNaN(saldo)) {
    throw new ParametrosInvalidosError();
  }

  if (dniAdmin !== Estado.ADMINISTRADOR) {
    throw new UsuarioNoHabilitadoError();
  }

  if (estado.claves[dniAdmin] !== claveAdmin) {
    throw new ClaveIncorrectaError();
  }

  // Persistencia de datos
  estado.saldo += saldo;
  estado.guardar();

  return 'ok';
};

export default carga;
