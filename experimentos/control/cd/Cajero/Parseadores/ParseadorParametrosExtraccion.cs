using System;

namespace Solucion;

public static class ParseadorParametrosExtraccion
{
    public static SolicitudExtraccion ParsearSolicitudExtraccion(this string[] args)
    {
        if (args.Length != 4)
        {
            throw new Exception("Sintaxis: extraccion <dni> <clave> <monto>");
        }
        else
        {
            return new SolicitudExtraccion(
                Dni: args[1],
                Clave: args[2],
                Monto: args[3]
            );
        }
    }
}
