import { autenticar } from "../utils.js";
import { Estado } from "../estado.js";

export const cambioDeClave = (dni, clave, nuevaClave) => {
  if (autenticar(dni, clave)) {
    const estado = Estado.cargar();
    const usuario = estado.usuarios.find((u) => u.dni === dni);
    if (usuario.clave === nuevaClave) {
      console.log("La nueva clave no puede ser igual a la actual.");
      return;
    }
    if (nuevaClave.length < 8) {
      console.log("La nueva clave debe tener al menos 8 caracteres.");
      return;
    }
    if (!nuevaClave.match(/[a-z]/i) || !nuevaClave.match(/[0-9]/)) {
      console.log("La nueva clave debe contener letras y números.");
      return;
    }

    const ultimoCambio = estado.movimientos
      .filter((mov) => mov.tipo === "clave" && mov.dni === dni)
      .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))[0];

    if (ultimoCambio) {
      const hoy = new Date();
      const fechaUltimoCambio = new Date(ultimoCambio.fecha);

      const mismoMesYAnio =
        hoy.getFullYear() === fechaUltimoCambio.getFullYear() &&
        hoy.getMonth() === fechaUltimoCambio.getMonth();

      if (mismoMesYAnio) {
        console.log("Solo se puede cambiar la clave una vez por mes.");
        return;
      }
    }

    usuario.clave = nuevaClave;

    const movimiento = {
      tipo: "clave",
      dni: usuario.dni,
      fecha: new Date().toISOString(),
    };
    estado.movimientos.push(movimiento);

    estado.guardar();

    console.log("Se cambió la clave correctamente.");
  } else {
    console.log("Autenticación fallida.");
  }
};
