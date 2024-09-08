import { autenticar, esAdmin } from "../utils.js";
import { Estado } from "../estado.js";

export const cargarSaldoCajero = (dni, clave, monto) => {
  if (autenticar(dni, clave) && esAdmin(dni)) {
    const estado = Estado.cargar();
    estado.cajero.saldo += monto;
    estado.guardar();
    console.log(`Se cargaron $${monto} al cajero.`);
  } else {
    console.log("Autenticación fallida.");
  }
};
