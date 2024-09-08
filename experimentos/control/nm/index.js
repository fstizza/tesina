import { Estado } from "./estado.js";

function validateAmount(args, num) {
  if (args.length < num) {
    console.log(
      `Cantidad erronea de argumentos para la operacion ${args[0]}, se obtuvieron ${args.length} pero se esperaban ${num}.`
    );
    process.exit(1);
  }
}

function showOperation(operation) {
  switch (operation) {
    case "withdraw":
      return "Retiro";
    case "deposit":
      return "Deposito";
    default:
      return "";
  }
}

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  const state = Estado.cargar();
  try {
    switch (args[0]) {
      case "extraccion":
        {
          validateAmount(args, 4);
          const dni = args[1];
          const password = args[2];
          const amount = +args[3];
          state.manager.withdraw(dni, password, amount);
          console.log("Extraccion exitosa");
        }
        break;
      case "clave":
        {
          validateAmount(args, 4);
          const dni = args[1];
          const password = args[2];
          const newPassword = args[3];
          state.manager.changePassword(dni, password, newPassword);
          console.log("Cambio de clave exitoso");
        }
        break;
      case "saldo":
        {
          validateAmount(args, 3);
          const dni = args[1];
          const password = args[2];
          const balance = state.manager.getBalance(dni, password);
          console.log(`El saldo que posee es de $${balance}`);
        }
        break;
      case "alta":
        {
          validateAmount(args, 8);
          const dniAdmin = args[1];
          const passwordAdmin = args[2];
          const dni = args[3];
          const password = args[4];
          const name = args[5];
          const salary = +args[6];
          const balance = +args[7];
          state.manager.newUser(
            dniAdmin,
            passwordAdmin,
            dni,
            password,
            name,
            salary,
            balance
          );
          console.log("Usuario creado exitosamente");
        }
        break;
      case "carga":
        {
          validateAmount(args, 4);
          const dniAdmin = args[1];
          const passwordAdmin = args[2];
          const amount = +args[3];
          state.manager.loadATM(dniAdmin, passwordAdmin, amount);
          console.log("Saldo cargado exitosamente");
        }
        break;
      case "movimientos":
        {
          validateAmount(args, 6);
          const dniAdmin = args[1];
          const passwordAdmin = args[2];
          const dni = args[3];
          const from = args[4];
          const to = args[5];
          const movements = state.manager.getMovements(
            dniAdmin,
            passwordAdmin,
            dni,
            new Date(from),
            new Date(to)
          );
          console.log("Los movimientos de la cuenta son los siguientes: ");
          movements.forEach((m) => {
            console.log(
              `${m.date} | ${showOperation(m.operation)}: $${
                m.amount
              }`
            );
          });
        }
        break;
      default:
        console.log("Operación inválida.");
        process.exit(1);
    }
    state.guardar();
    process.exit(0);
  } catch (error) {
    console.log(error.message);
    state.guardar();
    process.exit(1);
  }
}

main(process.argv.slice(2));
