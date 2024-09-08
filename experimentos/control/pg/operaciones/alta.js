import { autenticar, esAdmin } from "../utils.js";
import { Estado } from "../estado.js";

export const altaDeUsuario = (
  dniAdmin,
  claveAdmin,
  dni,
  clave,
  nombre,
  sueldo,
  saldo
) => {
  if (autenticar(dniAdmin, claveAdmin) && esAdmin(dniAdmin)) {
    const estado = Estado.cargar();
    if (sueldo !== saldo) {
      console.log(
        "El saldo inicial debe ser igual al sueldo mensual declarado."
      );
      return;
    }
    if (estado.usuarios.find((u) => u.dni === dni)) {
      console.log("Ya existe un usuario con ese DNI.");
      return;
    }
    if (estado.usuarios.length < 5) {
      estado.usuarios.push({
        dni: dni,
        nombre: nombre,
        clave: clave,
        sueldo: sueldo,
        saldo: saldo,
        admin: false,
      });
      estado.guardar();
      console.log(`Se dio de alta al usuario ${nombre} con DNI ${dni}.`);
    } else {
      console.log("No se pueden dar de alta más usuarios.");
    }
  } else {
    console.log("Autenticación fallida.");
  }
};
