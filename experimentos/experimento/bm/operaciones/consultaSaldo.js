import { Estado } from "../estado.js";
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioInexistenteError from '../errores/UsuarioInexistenteError.js';

const consultaSaldo = (args) => {
  const [_, dni, clave] = args;

  const estado = Estado.cargar();

  // Validaciones
  if (!estado.usuarios[dni]) {
    throw new UsuarioInexistenteError();
  }

  if (estado.claves[dni] !== clave) {
    throw new ClaveIncorrectaError();
  }

  return estado.saldos[dni];
};

export default consultaSaldo;
