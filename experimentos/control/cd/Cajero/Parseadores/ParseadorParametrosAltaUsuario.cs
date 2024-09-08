using System;

namespace Solucion;

public static class ParseadorParametrosAltaUsuario
{
    public static SolicitudAltaUsuario ParsearSolicitudAltaUsuario(this string[] args)
    {
        if (args.Length != 8)
        {
            throw new Exception("Sintaxis: alta <dni_administrador> <clave_administrador> <dni> <clave> <nombre> <sueldo> <saldo>");
        }
        else
        {
            return new SolicitudAltaUsuario(
                Dni_Administrador: args[1],
                Clave_Administrador: args[2],
                Dni: args[3],
                Clave: args[4],
                Nombre: args[5],
                Sueldo: args[6],
                Saldo: args[7]
            );
        }
    }
}
