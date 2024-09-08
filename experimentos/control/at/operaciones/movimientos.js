import { obtenerUsuario } from '../comunes/obtenerUsuario.js'


function dar_formato_fecha(fechaSinFormato) {
  return fechaSinFormato.split('-').map(e => Number(e))
}

// retorna 1 si fecha1 es mayor a fecha2, 0 si son iguales, -1 si es menor.
function comparar_fechas2(fecha1, fecha2) {
  if (fecha1[2] < fecha2[2]) return -1
  if (fecha1[2] > fecha2[2]) return 1
  // si llega aca el año es igual
  if (fecha1[1] < fecha2[1]) return -1
  if (fecha1[1] > fecha2[1]) return 1
  // si llega aca el año y el mes es igual
  if (fecha1[0] < fecha2[0]) return -1
  if (fecha1[0] > fecha2[0]) return 1
  // si llega aca son iguales
  return 0
}

function imprimir_movimientos(mov, desde, hasta) {
  for (let i = 0; i < mov.length; i++) {
    let mov_i = mov[i];
    let fecha_i = mov_i.fecha
    if (comparar_fechas2(fecha_i, desde) >= 0 && comparar_fechas2(fecha_i, hasta) <= 0) {
      let impresion_i = "- movimiento " + i + ": "
      for (var propiedad in mov_i) {
        if (mov_i.hasOwnProperty(propiedad)) {
          impresion_i = impresion_i + propiedad + ": " + mov_i[propiedad] + " - "
        }
      }
      console.log(impresion_i);
    }
  }
}

// haremos la funcion solicitada sabiendo que el arreglo de movimientos esta ordenado pues los movimientos
// se pushean en orden ascendente, tambien consideramos que el formato de las variables desde
// y hasta es el siguiente. numDia-numMes-numAño.

export function movimientos(e, dniAdmin, claveAdmin, dni, desde, hasta) {
  desde = dar_formato_fecha(desde);
  hasta = dar_formato_fecha(hasta);
  dni = Number(dni);
  let usuario = obtenerUsuario(e, dni)
  if (e.admin.dni === dniAdmin && e.admin.clave === claveAdmin && usuario && desde && hasta) {
    imprimir_movimientos(usuario.movTotales, desde, hasta);
  }
  else console.log("no se pueden imprimir los movimientos.")
}