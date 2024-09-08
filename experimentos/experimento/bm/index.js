import extraccion from './operaciones/extraccion.js';
import cambioClave from './operaciones/cambioClave.js';
import consultaSaldo from './operaciones/consultaSaldo.js';
import altaUsuario from './operaciones/altaUsuario.js';
import carga from './operaciones/carga.js';
import consultaMovimientos from './operaciones/consultaMovimientos.js';

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  try {
    let resultado;

    switch (args[0]) {
      case "extraccion":
        resultado = extraccion(args);
        break;
      case "clave":
        resultado = cambioClave(args);
        break;
      case "saldo":
        resultado = consultaSaldo(args);
        break;
      case "alta":
        resultado = altaUsuario(args);
        break;
      case "carga":
        resultado = carga(args);
        break;
      case "movimientos":
        resultado = consultaMovimientos(args);
        break;
      default:
        console.log("Operación inválida.");
        process.exit(1);
    }

    console.log('RESULTADO', resultado);
  } catch (error) {
    console.error(error.message);
  }
}

main(process.argv.slice(2));
