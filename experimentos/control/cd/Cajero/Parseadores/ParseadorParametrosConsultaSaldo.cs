using System;

namespace Solucion;

public static class ParseadorParametrosConsultaSaldo
{
    public static SolicitudConsultaSaldo ParsearSolicitudConsultaSaldo(this string[] args)
    {
        if (args.Length != 3)
        {
            throw new Exception("Sintaxis: saldo <dni> <clave>");
        }
        else
        {
            return new SolicitudConsultaSaldo(
                Dni: args[1], 
                Clave: args[2]
            );
        }
    }
}
