using System;

namespace Solucion;

public static class ParseadorParametrosCargaCajero
{
    public static SolicitudCargaCajero ParsearSolicitudCargaCajero(this string[] args)
    {
        if (args.Length != 4)
        {
            throw new Exception("Sintaxis: carga <dni_administrador> <clave_administrador> <monto>.");
        }
        else
        {
            return new SolicitudCargaCajero(
                Dni_Administrador: args[1], 
                Clave_Administrador: args[2], 
                Monto: args[3]
            );
        }
    }
}
