using System;

namespace Solucion;

public static class ParseadorParametrosCambioClave
{
    public static SolicitudCambioClave ParsearSolicitudCambioClave(this string[] args)
    {
        if (args.Length != 4)
        {
            throw new Exception("Sintaxis: clave <dni> <actual> <nueva>");
        }
        else
        {
            return new SolicitudCambioClave(
                Dni: args[1], 
                ClaveActual: args[2], 
                ClaveNueva: args[3]
            );
        }
    }
}
