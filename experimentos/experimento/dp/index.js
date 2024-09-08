import { AltaUsuario, Carga, ConsultaMovimientos, ConsultarSaldo, Extraccion, CambioClave } from "./operaciones.js";

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  let resp;

  switch (args[0]) {
    case "extraccion":
      console.log(Extraccion(args[1], args[2], args[3]));
      break;
    case "clave":
      console.log(CambioClave(args[1], args[2], args[3]));
      break;
    case "saldo":
      resp = ConsultarSaldo(args[1], args[2]);
      if(resp.saldo) {
        console.log("Saldo: " + resp.saldo);
      }
      console.log(resp.res);
      break;
    case "alta":
      console.log(AltaUsuario(args[1], args[2], args[3],args[4], args[5], args[6]));
      break;
    case "carga":
      console.log(Carga(args[1], args[2], args[3]));
      break;
    case "movimientos":
      resp = ConsultaMovimientos(args[1], args[2], args[3],args[4], args[5]);
      if(resp.movimientos) {
        console.log(JSON.stringify(resp.movimientos));
      }
      console.log(resp.res);
      break;
    default:
      console.log("Operación inválida.");
      process.exit(1);
  }

}

main(process.argv.slice(2));
