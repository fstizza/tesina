import { autenticar, esAdmin } from "../utils.js";
import { Estado } from "../estado.js";

const validarFormato = (fecha) => {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  return regex.test(fecha);
};

export const consultarMovimientos = (
  dniAdmin,
  clave,
  dniUsuario,
  fechaDesde,
  fechaHasta
) => {
  if (autenticar(dniAdmin, clave) && esAdmin(dniAdmin)) {
    const estado = Estado.cargar();
    const usuario = estado.usuarios.find((u) => u.dni === dniUsuario);

    if (!validarFormato(fechaDesde) || !validarFormato(fechaHasta)) {
      console.log("El formato de fecha debe ser AAAA-MM-DD.");
      return;
    }

    const movimientos = estado.movimientos.filter(
      (m) =>
        m.dni === dniUsuario &&
        new Date(m.fecha) >= new Date(fechaDesde) &&
        new Date(m.fecha) <= new Date(fechaHasta)
    );

    console.log(`Movimientos de ${usuario.nombre}:`);
    movimientos.forEach((m) => {
      console.log(
        `${m.fecha} - ${m.tipo} ${
          m.tipo === "extraccion" ? `- $${m.monto}` : ""
        }`
      );
    });
  } else {
    console.log("Autenticación fallida.");
  }
};
