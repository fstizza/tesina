import { Estado } from './estado.js';
import { consultarSaldoOK, extraccionOk, cambioClaveOk, consultarMovimientosOk, altaUsuarioOk, cargaOk } from './suboperaciones.js';

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }
  var estado = Estado.cargar();
  switch (args[0]) {
    case "extraccion":
      extraccionOk(args[1], args[2], args[3], estado);
      break;
    case "clave":
      cambioClaveOk(args[1], args[2], args[3], estado);
      break;
    case "saldo":
      consultarSaldoOK(args[1], args[2], estado);
      break;
    case "alta":
      altaUsuarioOk(args[1], args[2], args[3], args[4], args[5], args[6], estado);
      break;
    case "carga":
      cargaOk(args[1], args[2], args[3], estado)
      break;
    case "movimientos":
      consultarMovimientosOk(args[1], args[2], args[3], args[4], args[5], estado);
      break;
    default:
      console.log("Operación inválida.");
      process.exit(1);
  }
}

main(process.argv.slice(2));
