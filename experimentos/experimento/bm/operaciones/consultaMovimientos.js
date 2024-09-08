import { Estado } from "../estado.js";
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioInexistenteError from '../errores/UsuarioInexistenteError.js';
import UsuarioNoHabilitadoError from '../errores/UsuarioNoHabilitadoError.js';

const consultaMovimientos = (args) => {
  const [_, dniAdmin, claveAdmin, dniConsulta, desde, hasta] = args;

  const estado = Estado.cargar();

  // Validaciones
  if (dniAdmin !== Estado.ADMINISTRADOR) {
    throw new UsuarioNoHabilitadoError();
  }
  
  if (estado.claves[dniAdmin] !== claveAdmin) {
    throw new ClaveIncorrectaError();
  }

  if (!estado.usuarios[dniConsulta]) {
    throw new UsuarioInexistenteError();
  }

  const movimientos = estado.movimientos[dniConsulta].filter((movimiento) => new Date(movimiento.fechaHora) >= new Date(desde) && new Date(movimiento.fechaHora) <= new Date(hasta));

  return movimientos;
};

export default consultaMovimientos;
