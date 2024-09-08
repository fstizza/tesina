import { Cajero } from './cajero.js';

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  let cajero = new Cajero();

  switch (args[0]) {
    case "extraccion":
      cajero.extraccion(args[1], args[2], parseInt(args[3]));
      break;
    case "clave":
      cajero.cambioClave(args[1], args[2], args[3]);
      break;
    case "saldo":
      cajero.consultaSaldo(args[1], args[2]);
      break;
    case "alta":
      cajero.altaUsuario(args[1], args[2], args[3], args[4], args[5], parseInt(args[6]), parseInt(args[7]));
      break;
    case "carga":
      cajero.carga(args[1], args[2], parseInt(args[3]));
      break;
    case "movimientos":
      cajero.consultaMovimientos(args[1], args[2], args[3], args[4], args[5]);
      break;
    default:
      process.exit(1);
  }

  cajero.cerrar();
}

main(process.argv.slice(2));
