import { OPERACION } from "./enums.js";
import { Estado } from "./estado.js";
import { ahora } from "./globals.js";

export function MismoDia(fecha1, fecha2) {
    fecha1 = new Date(fecha1);
    fecha2 = new Date(fecha2);
    return fecha1.getDate() ==  fecha2.getDate() &&
        fecha1.getMonth() == fecha2.getMonth() &&
        fecha1.getFullYear() == fecha2.getFullYear() ? true : false;
}

export function MismoMes(fecha1, fecha2) {
    fecha1 = new Date(fecha1);
    fecha2 = new Date(fecha2);
    return fecha1.getMonth() == fecha2.getMonth() &&
        fecha1.getFullYear() == fecha2.getFullYear() ? true : false;
}

export function DifFechasDias(fecha1, fecha2) {
    fecha1 = new Date(fecha1);
    fecha2 = new Date(fecha2);
    return (fecha1 - fecha2) / (1000 * 60 * 60 * 24)
}

export function PerteneceACONTIENE_LETRA_NUM(texto) {
    let textoStr = texto + "";
    let i, len, code;

    for (i = 0, len = textoStr.length; i < len; i++) {
        code = textoStr.charCodeAt(i);
        if (!(code > 47 && code < 58) && // numeric (0-9)
            !(code > 64 && code < 91) && // upper alpha (A-Z)
            !(code > 96 && code < 123)) { // lower alpha (a-z)
          return false;
        }
      }
      return true;
}

export function LONGITUD(texto) {
    return texto.length;
}

export function CantidadExtraccionesHoy(dni) {
    let estado = Estado.cargar();

    return Object.getOwnPropertyNames(estado.movimientos[dni]).filter(a => estado.movimientos[dni][a] == OPERACION.extraccion && MismoDia(new Date(a), ahora)).length;
}

export function HayCambioDeClaveEsteMes(dni) {
    let estado = Estado.cargar();

    return Object.getOwnPropertyNames(estado.movimientos[dni]).some(a => estado.movimientos[dni][a] == OPERACION.clave && MismoMes(new Date(a), ahora));
}

export function ExisteUsuarioDNIConClave(dni, clave) {
    let estado = Estado.cargar();

    return estado.usuarios[dni] && 
    estado.claves[dni] == clave;
}
/*
external function MISMO MES : FECHAHORA → P FECHAHORA
Asigna a cada FECHAHORA un conjunto de FECHAHORA que corresponden al mismo mes y a˜no
del par´ametro.

external function MISMO DIA : FECHAHORA → P FECHAHORA
An´alogo al anterior, pero el conjunto de FECHAHORA corresponden al mismo d´ıa, mes y a˜no del
par´ametro.

external function DIF FECHAS DIAS : (FECHAHORA × FECHAHORA) → Z
Asigna a cada par (f1,f2) la diferencia en d´ıas entre f 1 − f 2.

external function LONGITUD : CLAVE → N
Asigna a cada clave la cantidad de caracteres que la compone.

external function CONTIENE LETRA NUM : P CLAVE
Es el conjunto de todas las posibles claves que son alfanum´ericas.
Nota: no es necesario que se implementen funciones que cumplan estas definiciones expl´ıcitamente.
Se pueden encontrar funciones que modelen lo que cada funci´on externa busca representar.
*/