import { Estado } from "./estado.js";

function main(args) {
  if (args.length === 0) {
    console.log("Sin argumentos.");
    process.exit(1);
  }

  let estado = Estado.cargar();

  let dniAdmin = '';
  let claveAdmin = '';
  let dniUsuario = '';
  let claveUsuario = '';
  let nombre = '';
  let sueldoUsuario = 0;
  let saldoUsuario = 0;
  let usuario = {};
  let monto = 0;
  let dias = 0;
  let diferencia = 0;
  let fechaActual = new Date();
  let fechaUltimaExtraccion = new Date();
  let fechaModificacionClave = null;

  switch (args[0]) {
    case "extraccion":

      dniUsuario = args[1];
      claveUsuario = args[2];
      monto = args[3];

      usuario = estado.usuarios.find((usuario) => usuario.dniUsuario === dniUsuario);

      if (!usuario) {
        console.log("Usuario inválido.");
        process.exit(1);
      }

      if (claveUsuario !== usuario.claveUsuario) {
        console.log("Clave inválida.");
        process.exit(1);
      }

      if (monto > usuario.saldoUsuario) {
        console.log("Saldo insuficiente.");
        process.exit(1);
      }

      if (monto > estado.saldoCajero) {
        console.log("Saldo insuficiente en el cajero.");
        process.exit(1);
      }

      fechaUltimaExtraccion = new Date(usuario.fechaUltimaExtraccion);
      diferencia = fechaActual.getTime() - fechaUltimaExtraccion.getTime();
      dias = Math.round(diferencia / (1000 * 3600 * 24));

      if (dias >= 1) {
        usuario.extraccionesHoy = 0;
      }

      if (usuario.extraccionesHoy >= 3) {
        console.log("El usuario ha alcanzado el límite de tres extracciones por día.");
        process.exit(1);
      } else if (monto > usuario.sueldoUsuario / 2) {
        console.log("El monto de la extracción no puede superar la mitad del sueldo.");
        process.exit(1);
      }
      usuario.extraccionesHoy++;
      
      console.log("Extracción exitosa.");
      usuario.saldoUsuario -= monto;
      estado.saldoCajero -= monto;
      usuario.fechaUltimaExtraccion = fechaActual.toISOString();
      usuario.movimientos.push({
        fecha: fechaActual.toISOString(),
        movimiento: "Extracción",
        monto: monto
      });
      estado.guardar();

      break;
    case "clave":

      dniUsuario = args[1];
      claveUsuario = args[2];
      let nuevaClave = args[3];

      usuario = estado.usuarios.find((usuario) => usuario.dniUsuario === dniUsuario);

      if (!usuario) {
        console.log("Usuario inválido.");
        process.exit(1);
      }

      if (claveUsuario !== usuario.claveUsuario) {
        console.log("Clave inválida.");
        process.exit(1);
      }

      if (nuevaClave.length < 8) {
        console.log("La clave debe tener al menos 8 caracteres.");
        process.exit(1);
      }

      if (!nuevaClave.match(/^[0-9a-zA-Z]+$/)) {
        console.log("La clave debe ser una combinación de letras y números.");
        process.exit(1);
      }

      if (usuario.fechaModificacionClave) {
        let fechaModificacion = new Date(usuario.fechaModificacionClave);
        diferencia = fechaActual.getTime() - fechaModificacion.getTime();
        dias = Math.round(diferencia / (1000 * 3600 * 24));

        if (dias < 30) {
          console.log("Solo puede modificar su clave una vez por mes.");
          process.exit(1);
        }
      }

      usuario.claveUsuario = nuevaClave;
      usuario.fechaModificacionClave = fechaActual;
      usuario.movimientos.push({
        fecha: fechaActual.toISOString(),
        movimiento: "Modificación de clave",
      });
      estado.guardar();

      break;
    case "saldo":

      dniUsuario = args[1];
      claveUsuario = args[2];

      usuario = estado.usuarios.find((usuario) => usuario.dniUsuario === dniUsuario);
      if (!usuario) {
        console.log("Usuario inválido.");
        process.exit(1);
      }

      if (claveUsuario !== usuario.claveUsuario) {
        console.log("Clave inválida.");
        process.exit(1);
      }

      console.log(`Saldo: ${usuario.saldoUsuario}`);
      usuario.movimientos.push({
        fecha: fechaActual.toISOString(),
        movimiento: "Consulta de saldo",
      });

      estado.guardar();

      break;

    case "alta":
      dniAdmin = args[1];
      claveAdmin = args[2];
      dniUsuario = args[3];
      claveUsuario = args[4];
      nombre = args[5];
      sueldoUsuario = args[6];
      saldoUsuario = args[7];

      if (dniAdmin !== estado.dniAdmin || claveAdmin !== estado.claveAdmin) {
        console.log("Administrador inválido.");
        process.exit(1);
      }

      if (saldoUsuario !== sueldoUsuario) {
        console.log("Saldo inicial debe ser igual al sueldo mensual declarado.");
        process.exit(1);
      }

      if (estado.usuarios.length >= 5) {
        console.log("No se pueden crear más usuarios.");
        process.exit(1);
      }

      usuario = {
        dniUsuario,
        claveUsuario,
        nombre,
        sueldoUsuario,
        saldoUsuario,
        fechaModificacionClave,
        fechaUltimaExtraccion,
        extraccionesHoy: 0,
        movimientos: []
      };

      estado.usuarios.push(usuario);
      estado.guardar();

      break;
    case "carga":
      dniAdmin = args[1];
      claveAdmin = args[2];
      monto = args[3];
    
      if (dniAdmin !== estado.dniAdmin || claveAdmin !== estado.claveAdmin) {
        console.log("Administrador inválido.");
        process.exit(1);
      }

      if(!monto) {
        console.log("Debe ingresar un monto.");
        process.exit(1);
      }
      estado.saldoCajero += parseInt(monto);
      estado.guardar();

      break;
    case "movimientos":
      // Formato para las fechas: AAAA-MM-DD ej : "2023-01-31"

      dniAdmin = args[1];
      claveAdmin = args[2];
      dniUsuario = args[3];
      let desde = args[4];
      let hasta = args[5];

      if (dniAdmin !== estado.dniAdmin || claveAdmin !== estado.claveAdmin) {
        console.log("Administrador inválido.");
        process.exit(1);
      }

      if (!dniUsuario) {
        console.log("Debe ingresar un dni de usuario.");
        process.exit(1);
      }

      if (!desde) {
        console.log("Debe ingresar una fecha desde.");
        process.exit(1);
      }

      if (!hasta) {
        console.log("Debe ingresar una fecha hasta.");
        process.exit(1);
      }

      usuario = estado.usuarios.find((usuario) => usuario.dniUsuario === dniUsuario);
      if (!usuario) {
        console.log("Usuario inválido.");
        process.exit(1);
      }

      let movimientos = usuario.movimientos.filter((movimiento) => {
        let fechaMovimiento = new Date(movimiento.fecha);
        let fechaDesde = new Date(desde);
        let fechaHasta = new Date(hasta);
        return fechaMovimiento >= fechaDesde && fechaMovimiento <= fechaHasta;
      });

      console.log(movimientos);

      break;
    default:
      console.log("Operación inválida.");
      process.exit(1);
  }
}

main(process.argv.slice(2));