import { altaDeUsuario } from "./operaciones/alta.js";
import { cambioDeClave } from "./operaciones/cambio-clave.js";
import { cargarSaldoCajero } from "./operaciones/carga.js";
import { consultarSaldo } from "./operaciones/consulta-saldo.js";
import { extraer } from "./operaciones/extraccion.js";
import { consultarMovimientos } from "./operaciones/movimientos.js";

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  switch (args[0]) {
    case "extraccion":
      extraer(args[1], args[2], parseInt(args[3]));
      break;
    case "clave":
      cambioDeClave(args[1], args[2], args[3]);
      break;
    case "saldo":
      consultarSaldo(args[1], args[2]);
      break;
    case "alta":
      altaDeUsuario(
        args[1],
        args[2],
        args[3],
        args[4],
        args[5],
        parseInt(args[6]),
        parseInt(args[7])
      );
      break;
    case "carga":
      cargarSaldoCajero(args[1], args[2], parseInt(args[3]));
      break;
    case "movimientos":
      consultarMovimientos(args[1], args[2], args[3], args[4], args[5]);
      break;
    default:
      console.log("Operación inválida.");
      process.exit(1);
  }
}

main(process.argv.slice(2));
