using System;

namespace Solucion
{
    public enum OPERACION
    {
        extraccion,
        clave
    }

    public enum RESULTADO
    {
        ok,
        usuarioInexistente,
        usuarioYaExistente,
        claveIncorrecta,
        saldoCajeroInsuficiente,
        saldoInsuficiente,
        noCumplePoliticaExtraccion,
        noCumplePoliticaExtraccion2,
        usuarioNoHabilitado,
        limiteUsuariosAlcanzado,
        cambioDeClaveBloqueado,
        noCumpleRequisitosClave1,
        noCumpleRequisitosClave2,
    }
}
