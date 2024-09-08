import { obtenerUsuario } from '../comunes/obtenerUsuario.js'
import { Extraccion } from '../estado.js';
import { crearFecha } from '../comunes/crearFecha.js'

// compara dos fechas. retorna true si son iguales, caso contrario false.
function comparar_fecha(fecha1,fecha2) {
  return fecha1[0] === fecha2[0] && fecha1[1] === fecha2[1] && fecha1[2] === fecha2[2];
}

// retorna el usuario con las extracciones del dia actualizadas.
function insertar_extHoy(usuario, ext) {
  if (usuario.extHoy.length === 0) {
    usuario.extHoy.push(ext);
  }
  else {
    let fechaUltExt = usuario.extHoy[0].fecha;
    let fechaActExt = ext.fecha;
    if (comparar_fecha(fechaUltExt, fechaActExt)) {
      usuario.extHoy.push(ext)
    }
    else {
      usuario.extHoy = [ext]
    }
  }
  return usuario
}

// retorna true si la extraccion se puede realizar, caso contrario false.
function extraccion_realizable(e, usuario, monto, fecha) {
  if (e.fondos < monto) return false
  if (usuario.sueldo/2 < monto) return false
  if (usuario.extHoy.length >= 3 && comparar_fecha(usuario.extHoy[0].fecha, fecha)) return false
  if (usuario.saldo < monto) return false
  return true
}
// función solicitada para que un usuario pueda extraer el dinero del cajero.
export function extraccion(e, dni, clave, monto) {
  dni = Number(dni);
  monto = Number(monto);
  let fecha = crearFecha();
  let usuario = obtenerUsuario(e, dni);
  if (usuario && usuario.clave === clave && extraccion_realizable(e, usuario, monto, fecha)) {
    let ext = new Extraccion(monto, fecha);
    usuario = insertar_extHoy(usuario, ext);
    usuario.movTotales.push(ext);
    usuario.saldo = usuario.saldo - monto;
    e.fondos = e.fondos - monto;
    console.log("extraccion realizada con éxito");
  }
  else console.log("extraccion no realizada.")
  return e;
}