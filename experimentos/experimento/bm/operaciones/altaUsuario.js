import { Estado } from "../estado.js";
import UsuarioNoHabilitadoError from '../errores/UsuarioNoHabilitadoError.js';
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioYaExistenteError from '../errores/UsuarioYaExistenteError.js';
import LimiteUsuariosAlcanzadoError from '../errores/LimiteUsuariosAlcanzadoError.js';

// node index.js alta 42325945 Password1! 43285891 Password1! Milagros 1000 150
const altaUsuario = (args) => {
  const [_, dniAdmin, claveAdmin, dniUsuario, claveUsuario, nombreUsuario, sueldoUsuario] = args;

  const estado = Estado.cargar();

  // Validaciones
  if (dniAdmin !== Estado.ADMINISTRADOR) {
    throw new UsuarioNoHabilitadoError();
  }

  if (estado.claves[dniAdmin] !== claveAdmin) {
    throw new ClaveIncorrectaError();
  }

  if (estado.usuarios[dniUsuario]) {
    throw new UsuarioYaExistenteError();
  }

  if (Object.keys(estado.usuarios).length >= Estado.CANT_MAX_USUARIOS) {
    throw new LimiteUsuariosAlcanzadoError();
  }

  // Persistencia de datos
  estado.usuarios[dniUsuario] = nombreUsuario;
  estado.claves[dniUsuario] = claveUsuario;
  estado.saldos[dniUsuario] = sueldoUsuario;
  estado.sueldos[dniUsuario] = sueldoUsuario;
  estado.guardar();

  return 'ok';
};

export default altaUsuario;
