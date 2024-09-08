import { Resultado, claveAdministrador } from './constantes.js';
import { Movimiento } from './movimiento.js';
import { Operacion, ahora, administrador, cantMaxUsuarios, longMinClave } from './constantes.js';

export function consultarSaldoOK(dni, clave, estado) {
  if (estado.usuarios.includes(dni)) {
    let index = estado.usuarios.findIndex(u => u == dni);
    if (estado.claves[index] == clave) {
      return console.log(estado.saldos[index]);
    } else {
      return console.log(Resultado.ClaveIncorrecta);
    }
  } else {
    return console.log(Resultado.UsuarioInexistente);
  }

}

export function extraccionOk(dni, clave, monto, estado) {
  monto = Number(monto)
  if (estado.usuarios.includes(dni)) {
    let index = estado.usuarios.findIndex(u => u == dni);
    if (estado.claves[index] == clave) {
      let extraccionesDelDia = _obtenerMovimientosDia(estado.movimientos[index], Operacion.Extraccion);
      if (extraccionesDelDia > 2) {
        return console.log(Resultado.NoCumplePoliticaExtraccion)
      }
      else if (monto > estado.sueldos[index] / 2) {
        return console.log(Resultado.NoCumplePoliticaExtraccion2)
      } else if (monto > estado.saldos[index]) {
        return console.log(Resultado.SaldoInsuficiente)
      } else if (monto > estado.saldo) {
        return console.log(Resultado.SaldoCajeroInsuficiente)
      } else {
        estado.saldos[index] -= monto;
        estado.movimientos[index].push(new Movimiento(Operacion.Extraccion, ahora));
        estado.saldo -= monto;
        estado.guardar();
        return console.log(Resultado.Ok);
      }
    } else {
      return console.log(Resultado.ClaveIncorrecta)
    }
  } else {
    return console.log(Resultado.UsuarioInexistente);
  }
}

export function cambioClaveOk(dni, clave, nuevaClave, estado) {
  if (estado.usuarios.includes(dni)) {
    let index = estado.usuarios.findIndex(u => u == dni);
    if (estado.claves[index] == clave) {
      if (_obtenerMovimientosMes(estado.movimientos[index], Operacion.Clave) == 0) {
        if (nuevaClave.length >= longMinClave) {
          if (/\d/.test(nuevaClave) && /[a-zA-Z]/.test(nuevaClave)) {
            estado.claves[index] = nuevaClave;
            estado.movimientos[index].push(new Movimiento(Operacion.Clave, ahora));
            estado.guardar();
            return console.log(Resultado.Ok);
          } else {
            return console.log(Resultado.NoCumpleRequisitoClave2);
          }
        } else {
          return console.log(Resultado.NoCumpleRequisitoClave1);
        }
      } else {
        return console.log()
      }
    } else {
      return console.log(Resultado.ClaveIncorrecta);
    }
  } else {
    return console.log(Resultado.UsuarioInexistente);
  }
}

export function consultarMovimientosOk(dni, clave, dniConsulta, desde, hasta, estado) {
  if (dni == administrador && clave == claveAdministrador) {
    if (estado.usuarios.includes(dniConsulta)) {
      let index = estado.usuarios.findIndex(u => u == dniConsulta);
      let movimientos = estado.movimientos[index].filter(m => {
        let fechaMovimiento = new Date(m.fecha * 1000);
        let fechaDesde = new Date(desde);
        let fechaHasta = new Date(hasta);
        return fechaMovimiento.getTime() >= fechaDesde.getTime() && fechaMovimiento.getTime() <= fechaHasta.getTime();
      });

      return console.log(movimientos);

    } else {
      return console.log(Resultado.UsuarioInexistente);
    }
  } else {
    return console.log(Resultado.UsuarioNoHabilitado);
  }
}

export function altaUsuarioOk(dniAdm, claveAdm, dni, clave, nombre, sueldo, estado) {
  if (dniAdm == administrador) {
    if (claveAdm == claveAdministrador) {
      if (estado.usuarios.includes(dni)) {
        return console.log(Resultado.UsuarioYaExistente);
      } else {
        if (estado.usuarios.length >= cantMaxUsuarios) {
          return console.log(Resultado.LimiteUsuarioAlcanzado);
        } else {
          estado.movimientos.push([]);
          estado.usuarios.push(dni);
          estado.claves.push(clave);
          estado.saldos.push(sueldo);
          estado.sueldos.push(sueldo);
          estado.guardar();
          return console.log(Resultado.Ok);
        }
      }
    } else {
      console.log(Resultado.ClaveIncorrecta)
    }
  } else {
    console.log(Resultado.UsuarioNoHabilitado);
  }
}

export function cargaOk(dniAdm, claveAdm, saldo, estado) {
  saldo = Number(saldo)
  if (dniAdm == administrador) {
    if (claveAdm == claveAdministrador) {
      estado.saldo += saldo;
      estado.guardar();
      return console.log(Resultado.Ok)
    } else {
      return console.log(Resultado.ClaveIncorrecta);
    }
  } else {
    return console.log(Resultado.UsuarioNoHabilitado)
  }
}

function _obtenerMovimientosDia(movimientos, tipoMovimiento) {
  return movimientos.filter(mov => {
    let fecha = new Date(mov.fecha * 1000);
    let fechaAhora = new Date(ahora * 1000);
    return mov.operacion == tipoMovimiento && mov.fecha &&
      (fecha.getDate() == fechaAhora.getDate() && fecha.getMonth() == fechaAhora.getMonth() && fecha.getFullYear() == fechaAhora.getFullYear())
  });
}

function _obtenerMovimientosMes(movimientos, tipoMovimiento) {
  return movimientos.filter(mov => {
    let fecha = new Date(mov.fecha * 1000);
    let fechaAhora = new Date(ahora * 1000);
    return mov.operacion == tipoMovimiento &&
      (fecha.getMonth() == fechaAhora.getMonth() && fecha.getFullYear() == fechaAhora.getFullYear());
  });
}
