import { CambioDeClaveBloqueado, ClaveIncorrecta, LimiteUsuariosAlcanzado, NoCumplePoliticaExtraccion, NoCumplePoliticaExtraccion2, NoCumpleRequisitosClave1, NoCumpleRequisitosClave2, SaldoCajeroInsuficiente, SaldoInsuficiente, UsuarioInexistente, UsuarioNoHabilitado, UsuarioYaExistente } from "./errores.js"
import { AltaUsuarioOK, CambioClaveOK, CargaOK, ConsultaMovimientosOK, ConsultaSaldoOK, ExtraccionOK } from "./suboperaciones.js"

export function Extraccion(dni, clave, monto) {

    return UsuarioInexistente(dni) ??
        ClaveIncorrecta(dni, clave) ??
        NoCumplePoliticaExtraccion(dni) ??
        NoCumplePoliticaExtraccion2(dni, monto) ??
        SaldoInsuficiente(dni, monto) ??
        SaldoCajeroInsuficiente(monto) ??
        ExtraccionOK(dni, clave, monto);
}

export function CambioClave(dni, clave, nueva_clave) {
    return NoCumpleRequisitosClave2(nueva_clave) ??
        UsuarioInexistente(dni) ??
        ClaveIncorrecta(dni, clave) ??
        CambioDeClaveBloqueado(dni) ??
        NoCumpleRequisitosClave1(nueva_clave) ??
        CambioClaveOK(dni, clave, nueva_clave);
}

export function ConsultarSaldo(dni, clave) {
    let res = UsuarioInexistente(dni) ?? ClaveIncorrecta(dni, clave);

    if (res) {
        return {
            "res": res
        }
    } else {
        return ConsultaSaldoOK(dni, clave);
    }

}

export function AltaUsuario(dniAdministrador, clave_administrador, dni, clave, nombre, sueldo) {
    return UsuarioNoHabilitado(dniAdministrador) ??
        ClaveIncorrecta(dniAdministrador, clave_administrador) ??
        UsuarioYaExistente(dni) ??
        LimiteUsuariosAlcanzado() ??
        AltaUsuarioOK(dniAdministrador, clave_administrador, dni, clave, nombre, sueldo);
}

export function Carga(dni, clave, saldo) {
    return ClaveIncorrecta(dni, clave) ??
        UsuarioNoHabilitado(dni) ??
        CargaOK(dni, clave, saldo);
}

export function ConsultaMovimientos(dni, clave, dniConsulta, desde, hasta) {
    let res = UsuarioNoHabilitado(dni) ?? UsuarioInexistente(dniConsulta) ?? ClaveIncorrecta(dni, clave);
    if (res) {
        return {
            "res": res
        };
    }
    else {
        return ConsultaMovimientosOK(dni, clave, dniConsulta, desde, hasta);
    }
}