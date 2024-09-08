using System;
using System.Linq;

namespace Solucion;

/// <remarks>
/// Clave del administrador: adm1n1strad0r
/// </remarks>
/// 
public class Programa
{
    public static void Main(string[] args)
    {
        if (!args.Any())
        {
            Console.WriteLine("Sin argumentos.");
            System.Environment.Exit(1);
        }

        try
        {
            var cajero = CajeroFactoria.InstanciarCajero();

            switch (args[0])
            {
                case "extraccion":
                    var resultadoExtraccion = cajero.Extraccion(args.ParsearSolicitudExtraccion());
                    Console.WriteLine(resultadoExtraccion.Mensaje);
                    break;
                case "clave":
                    var resultadoCambioClave = cajero.CambioClave(args.ParsearSolicitudCambioClave());
                    Console.WriteLine(resultadoCambioClave.Mensaje);
                    break;
                case "saldo":
                    var resultadoConsultaSaldo = cajero.ConsultaSaldo(args.ParsearSolicitudConsultaSaldo());
                    Console.WriteLine($"{resultadoConsultaSaldo.Mensaje} Saldo: ${resultadoConsultaSaldo.Saldo}");
                    break;
                case "alta":
                    var resultadoAltaUsuario = cajero.AltaUsuario(args.ParsearSolicitudAltaUsuario());
                    Console.WriteLine(resultadoAltaUsuario.Mensaje);
                    break;
                case "carga":
                    var resultadoCargaCajero = cajero.CargaCajero(args.ParsearSolicitudCargaCajero());
                    Console.WriteLine(resultadoCargaCajero.Mensaje);
                    break;
                case "movimientos":
                    var resultadoConsultaMovimientos = cajero.ConsultaMovimientos(args.ParsearSolicitudConsultaMovimientos());
                    Console.WriteLine(resultadoConsultaMovimientos.Mensaje);
                    if (resultadoConsultaMovimientos.Movimientos?.Count() > 0)
                    {
                        Console.WriteLine($"|      Fecha       |       Tipo      |    Importe   |");
                        Console.WriteLine($"|------------------|-----------------|--------------|");
                        foreach (var movimiento in resultadoConsultaMovimientos.Movimientos)
                        {
                            Console.WriteLine($"| {movimiento.Fecha:dd/MM/yyyy HH:mm} | {movimiento.Tipo,-15} | {Math.Abs(movimiento.Importe),12:F2} |");
                        }
                    }
                    break;
                default:
                    Console.WriteLine("Operación inválida.");
                    System.Environment.Exit(1);
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
            System.Environment.Exit(1);
        }
    }
}
