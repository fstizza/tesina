import { autenticar } from "../utils.js";
import { Estado } from "../estado.js";

export const extraer = (dni, clave, monto) => {
  if (autenticar(dni, clave)) {
    const estado = Estado.cargar();
    const usuario = estado.usuarios.find((u) => u.dni === dni);
    const cajero = estado.cajero;

    const hoy = new Date();
    const fechaHoy = hoy.toISOString().split("T")[0];
    const movimientosHoy = estado.movimientos.filter(
      (m) => m.dni === dni && m.fecha.split("T")[0] === fechaHoy
    );
    const extraccionesHoy = movimientosHoy.filter(
      (m) => m.tipo === "extraccion"
    );
    const montoMaximo = usuario.sueldo / 2;
    if (monto > montoMaximo) {
      console.log(`El monto máximo por extracción es $${montoMaximo}.`);
      return;
    }
    if (monto > cajero.saldo) {
      console.log("El cajero no tiene suficiente dinero.");
      return;
    }
    if (extraccionesHoy.length >= 3) {
      console.log("Solo se pueden hacer tres extracciones por día.");
      return;
    }
    if (usuario.saldo < monto) {
      console.log("El usuario no tiene suficiente saldo.");
      return;
    }
    usuario.saldo -= monto;
    cajero.saldo -= monto;
    estado.movimientos.push({
      tipo: "extraccion",
      dni: dni,
      fecha: hoy.toISOString(),
      monto: monto,
    });
    estado.guardar();
    console.log(`Se extrajeron $${monto}.`);
  } else {
    console.log("Autenticación fallida.");
  }
};
