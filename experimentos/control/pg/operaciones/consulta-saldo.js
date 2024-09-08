import { autenticar } from "../utils.js";
import { Estado } from "../estado.js";

export const consultarSaldo = (dni, clave) => {
  if (autenticar(dni, clave)) {
    const estado = Estado.cargar();
    const usuario = estado.usuarios.find((u) => u.dni === dni);
    console.log(`Saldo: $${usuario.saldo}`);
  } else {
    console.log("Autenticación fallida.");
  }
};
