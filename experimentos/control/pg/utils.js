import { Estado } from "./estado.js";

export const autenticar = (dni, clave) => {
  const estado = Estado.cargar();
  const usuario = estado.usuarios.find((u) => u.dni === dni);
  return usuario && usuario.clave === clave;
};

export const esAdmin = (dni) => {
  const estado = Estado.cargar();
  const usuario = estado.usuarios.find((u) => u.dni === dni);
  return usuario && usuario.admin;
};
