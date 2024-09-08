function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  switch (args[0]) {
    case "extraccion":
      // TODO: Completar.
      break;
    case "clave":
      // TODO: Completar.
      break;
    case "saldo":
      // TODO: Completar.
      break;
    case "alta":
      // TODO: Completar.
      break;
    case "carga":
      // TODO: Completar.
      break;
    case "movimientos":
      // TODO: Completar.
      break;
    default:
      console.log("Operación inválida.");
      process.exit(1);
  }
}

main(process.argv.slice(2));
