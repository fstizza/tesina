import { Estado } from "../estado.js";
import ClaveIncorrectaError from '../errores/ClaveIncorrectaError.js';
import UsuarioInexistenteError from '../errores/UsuarioInexistenteError.js';
import CambioDeClaveBloqueadoError from '../errores/CambioDeClaveBloqueadoError.js';
import NoCumpleRequisitosClave1 from '../errores/NoCumpleRequisitosClave1.js';
import NoCumpleRequisitosClave2 from '../errores/NoCumpleRequisitosClave2.js';
import isDatesMonthEqual from '../utils/isDatesMonthEqual.js';

const cambioClave = (args) => {
  const [_, dni, clave, nuevaClave] = args;

  const estado = Estado.cargar();

  // Validaciones
  if (!estado.usuarios[dni]) {
    throw new UsuarioInexistenteError();
  }

  if (estado.claves[dni] !== clave) {
    throw new ClaveIncorrectaError();
  }

  const movimientos = estado.movimientos[dni];
  const hoy = new Date().toISOString();
  if (movimientos && movimientos.filter((movimiento) => movimiento.operacion === 'clave' && isDatesMonthEqual(hoy, movimiento.fechaHora)).length > 0) {
    throw new CambioDeClaveBloqueadoError();
  }

  if (nuevaClave.length < Estado.LONG_MIN_CLAVE) {
    throw new NoCumpleRequisitosClave1();
  }

  if (!new RegExp('^[a-zA-Z0-9]*$').test(nuevaClave)) {
    throw new NoCumpleRequisitosClave2();
  }

  // Persistencia de datos
  estado.claves[dni] = nuevaClave;
  estado.movimientos[dni] = [
    ...(estado.movimientos[dni] || []),
    { 
      fechaHora: new Date().toISOString(), 
      operacion: 'clave' 
    },
  ];
  estado.guardar();

  return 'ok';
};

export default cambioClave;
