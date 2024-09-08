using System;
using System.Globalization;

namespace Solucion;

public static class ParseadorParametrosConsultaMovimientos
{
    public static SolicitudConsultaMovimientos ParsearSolicitudConsultaMovimientos(this string[] args)
    {
        if (args.Length != 6)
        {
            throw new Exception("Sintaxis: movimientos <dni_administrador> <clave_administrador> <dni_consulta> <desde> <hasta>");
        }
        else
        {
            var esAR = CultureInfo.GetCultureInfo("es-AR");
            return new SolicitudConsultaMovimientos(
                Dni_Administrador: args[1],
                Clave_Administrador: args[2],
                Dni_Consulta: args[3],
                Desde: DateOnly.Parse(args[4], esAR),
                Hasta: DateOnly.Parse(args[5], esAR)
            );
        }
    }
}
