import { OPERACION, RESULTADO } from "./enums.js";
import { Estado } from "./estado.js";
import { CantidadExtraccionesHoy, DifFechasDias, ExisteUsuarioDNIConClave, HayCambioDeClaveEsteMes, LONGITUD, PerteneceACONTIENE_LETRA_NUM } from "./functions.js";
import * as global from "./globals.js";

export function ConsultaSaldoOK(dni, clave ) {
    if(ExisteUsuarioDNIConClave(dni, clave)) { 
        let estado = Estado.cargar();

        return {
            "saldo": estado.saldos[dni],
            "res": RESULTADO.ok
        }
    }

}

export function ExtraccionOK(dni, clave, monto) {
    let estado = Estado.cargar();

    if (ExisteUsuarioDNIConClave(dni, clave) &&
    CantidadExtraccionesHoy(dni) <= 2 &&
    +monto <= +estado.sueldos[dni] / 2 &&
    +monto <= +estado.saldos[dni]) {
        estado.saldos[dni] = estado.saldos[dni] - monto;
        
        if(!estado.movimientos[dni]) { 
            estado.movimientos[dni] = {};
        }
        
        estado.movimientos[dni][global.ahora.toJSON()] = OPERACION.extraccion;
        estado.guardar();

        return RESULTADO.ok;
    } 
}

export function CambioClaveOK(dni, clave, nuevaClave) {
    let estado = Estado.cargar();

    if (ExisteUsuarioDNIConClave(dni, clave) &&
    LONGITUD(nuevaClave) >= global.LONG_MIN_CLAVE &&
    PerteneceACONTIENE_LETRA_NUM(nuevaClave) &&
    HayCambioDeClaveEsteMes(dni)) {
        estado.claves[dni] = nuevaClave;
        estado.movimientos[dni][global.ahora.toJSON()] = OPERACION.clave;
        estado.guardar();

        return RESULTADO.ok;
    }
}

export function ConsultaMovimientosOK(dni, clave, dniConsulta, desde, hasta) {
    let estado = Estado.cargar();

    if(dni == global.administrador && 
        estado.claves[dni] == clave &&
        estado.usuarios[dniConsulta]) {
            return {
                "movimientos": Object.getOwnPropertyNames(estado.movimientos[dniConsulta])
                .filter(x => DifFechasDias(x, desde) >= 0 && DifFechasDias(hasta, x))
                .map(f => {
                    debugger;
                    return f +": "+ estado.movimientos[dniConsulta][f];
                }),
                "res": RESULTADO.ok
            }
        }
}

export function AltaUsuarioOK(dniAdministrador, claveAdministrador, dni, clave, nombre, sueldo) {
    let estado = Estado.cargar();

    if(dniAdministrador == global.administrador &&
        estado.claves[dniAdministrador] == claveAdministrador &&
        !estado.usuarios[dni] &&
        Object.getOwnPropertyNames(estado.usuarios).length < 5) {
            estado.movimientos[dni] = {};
            estado.usuarios[dni] = nombre;
            estado.claves[dni] = clave;
            estado.saldos[dni] = sueldo;
            estado.sueldos[dni] = sueldo;

            estado.guardar();
            
            return RESULTADO.ok;
        }
}

export function CargaOK(dniAdministrador, claveAdministrador, saldo) {
    let estado = Estado.cargar();

    if(dniAdministrador == global.administrador &&
        estado.claves[dniAdministrador] == claveAdministrador) {
            estado.saldo = +estado.saldo + +saldo;
            estado.guardar();
            
            return RESULTADO.ok;
        }
}