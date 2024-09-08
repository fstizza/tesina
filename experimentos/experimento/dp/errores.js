import { Estado } from "./estado.js";
import { RESULTADO } from "./enums.js";
import { CantidadExtraccionesHoy, HayCambioDeClaveEsteMes, LONGITUD, PerteneceACONTIENE_LETRA_NUM } from "./functions.js";
import { LONG_MIN_CLAVE, administrador } from "./globals.js";

export function UsuarioInexistente(dni) {
    let estado = Estado.cargar();

    if(!estado.usuarios[dni]) {
        return RESULTADO.usuarioInexistente;
    }
}

export function UsuarioYaExistente(dni) {
    let estado = Estado.cargar();

    if(estado.usuarios[dni]) {
        return RESULTADO.usuarioYaExistente;    
    }
}

export function ClaveIncorrecta(dni, clave) {
    let estado = Estado.cargar();

    if(estado.claves[dni] && estado.claves[dni] != clave) {
        return RESULTADO.claveIncorrecta;
    }
}

export function SaldoCajeroInsuficiente(monto) {
    let estado = Estado.cargar();

    if(+monto > +estado.saldo) {
    return RESULTADO.saldoCajeroInsuficiente;
    }
}

export function SaldoInsuficiente(dni, monto) {
    let estado = Estado.cargar();

    if(estado.saldos[dni] != undefined && +monto > +estado.saldos[dni]) {
        return RESULTADO.saldoInsuficiente;
    }
}

export function NoCumplePoliticaExtraccion(dni) {
    let estado = Estado.cargar();

    if(estado.movimientos[dni] && CantidadExtraccionesHoy(dni) > 2) {
        return  RESULTADO.noCumplePoliticaExtraccion;
    }
}

export function NoCumplePoliticaExtraccion2(dni, monto) {
    let estado = Estado.cargar();

    if(estado.sueldos[dni] && +monto > (+estado.sueldos[dni] / 2)) {
        return  RESULTADO.noCumplePoliticaExtraccion2;
    }
}

export function LimiteUsuariosAlcanzado() {
    let estado = Estado.cargar();

    if(Object.getOwnPropertyNames(estado.usuarios).length >= 5) {
        return  RESULTADO.limiteUsuariosAlcanzado;
    }
}

export function CambioDeClaveBloqueado(dni) {
    let estado = Estado.cargar();

    if(estado.movimientos[dni] && HayCambioDeClaveEsteMes(dni) >= 0) {
        return RESULTADO.cambioDeClaveBloqueado;
    }
}

export function UsuarioNoHabilitado(dni) {
    if(dni != administrador) {
        return RESULTADO.usuarioNoHabilitado;
    }
}

export function NoCumpleRequisitosClave1(clave) {
    if(LONGITUD(clave) < LONG_MIN_CLAVE) {
        return RESULTADO.noCumpleRequisitosClave1;
    }
}

export function NoCumpleRequisitosClave2(clave) {
    if(!PerteneceACONTIENE_LETRA_NUM(clave)) {
        return RESULTADO.noCumpleRequisitosClave2;
    }
}