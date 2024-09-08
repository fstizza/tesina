using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading;

namespace Solucion;

public class Programa
{

    public static void Main(string[] args)
    {
        if (!args.Any())
        {
            Console.WriteLine("Sin argumentos.");
            System.Environment.Exit(1);
        }

        switch (args[0])
        {
            case "ayuda":
                EjecutarAyuda();
                break;
            case "extraccion":
                EjecutarExtraccion(args);
                break;
            case "clave":
                EjecutarClave(args);
                break;
            case "saldo":
                EjecutarSaldo(args);
                break;
            case "alta":
                EjecutarAlta(args);
                break;
            case "carga":
                EjecutarCarga(args);
                break;
            case "movimientos":
                EjecutarMovimientos(args);
                break;
            default:
                Console.WriteLine("Operación inválida.");
                System.Environment.Exit(1);
                break;
        }


    }

    private static void EjecutarAyuda()
    {
        Console.WriteLine("extraccion <DNI> <CLAVE> <MONTO>");
        Console.WriteLine("clave <DNI> <CLAVE> <NUEVA_CLAVE>");
        Console.WriteLine("saldo <DNI> <CLAVE>");
        Console.WriteLine("alta <DNI_Admin> <CLAVE_Admin> <DNI> <CLAVE> <NOMBRE> <SUELDO>");
        Console.WriteLine("carga <DNI> <CLAVE> <MONTO>");
        Console.WriteLine("movimientos <DNI> <CLAVE> <DNI_Consulta> <FECHAHORA_Desde> <FECHAHORA_Hasta>");
    }

    private static void EjecutarExtraccion(string[] args)
    {
        int? DNI = null;
        string CLAVE = null;
        decimal? MONTO = null;

        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[2];
        if (decimal.TryParse(args[3], out decimal decimalMONTO)) { MONTO = decimalMONTO; }

        var respuesta = Operaciones.Extraccion(DNI, CLAVE, MONTO);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine("La extacción se realizó satisfactoriamente.");
        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }
    }

    private static void EjecutarClave(string[] args)
    {
        int? DNI = null;
        string CLAVE = null;
        string NUEVA_CLAVE = null;

        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[2];
        NUEVA_CLAVE = args[3];

        var respuesta = Operaciones.CambioClave(DNI, CLAVE, NUEVA_CLAVE);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine("El cambio de clave se realizó satisfactoriamente.");
        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }
    }

    private static void EjecutarSaldo(string[] args)
    {
        int? DNI = null;
        string CLAVE = null;
        decimal? MONTO = null;

        if (args.Length < 3) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[2];

        var respuesta = Operaciones.ConsultaSaldo(DNI, CLAVE, ref MONTO);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine($"Saldo disponible = {MONTO}.");
        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }
    }

    private static void EjecutarAlta(string[] args)
    {
        int? DNI_Admin = null;
        string CLAVE_Admin = null;
        int? DNI = null;
        string CLAVE = null;
        string NOMBRE = null;
        decimal? SUELDO = null;

        if (args.Length < 7) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI_Admin)) { DNI_Admin = intDNI_Admin; }
        CLAVE_Admin = args[2];
        if (int.TryParse(args[3], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[4];
        NOMBRE = args[5];
        if (decimal.TryParse(args[6], out decimal decimalSUELDO)) { SUELDO = decimalSUELDO; }

        var respuesta = Operaciones.AltaUsuario(DNI_Admin, CLAVE_Admin, DNI, CLAVE, NOMBRE, SUELDO);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine("El alta de usuario se realizó satisfactoriamente.");
        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }
    }

    private static void EjecutarCarga(string[] args)
    {
        int? DNI = null;
        string CLAVE = null;
        decimal? MONTO = null;

        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[2];
        if (decimal.TryParse(args[3], out decimal decimalMONTO)) { MONTO = decimalMONTO; }

        var respuesta = Operaciones.Carga(DNI, CLAVE, MONTO);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine("La carga se realizó satisfactoriamente.");
        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }
    }

    private static void EjecutarMovimientos(string[] args)
    {
        int? DNI = null;
        string CLAVE = null;
        int? DNI_Consulta = null;
        DateTime? FECHAHORA_Desde = null;
        DateTime? FECHAHORA_Hasta = null;
        List<Operacion> MOVIMIENTOS = null;

        if (args.Length < 6) { Console.WriteLine("Faltan argumentos para la operación."); }

        if (int.TryParse(args[1], out int intDNI)) { DNI = intDNI; }
        CLAVE = args[2];
        if (int.TryParse(args[3], out int intDNIConsulta)) { DNI_Consulta = intDNIConsulta; }
        if (DateTime.TryParse(args[4], out DateTime dateDESDE)) { FECHAHORA_Desde = dateDESDE; }
        if (DateTime.TryParse(args[5], out DateTime dateHASTA)) { FECHAHORA_Hasta = dateHASTA; }

        var respuesta = Operaciones.ConsultaMovimientos(DNI, CLAVE, DNI_Consulta, FECHAHORA_Desde, FECHAHORA_Hasta, ref MOVIMIENTOS);

        if (respuesta.Resultado == ResultadoOperacion.Resultados.OK)
        {
            Console.WriteLine("La consulta de movimientos se realizó satisfactoriamente.");
            Console.WriteLine(" ");
            Console.WriteLine($"| Fecha operación  | Tipo operación       | Movimiento | Resultado            | Saldo    |");
            foreach (var item in MOVIMIENTOS)
            {
                Console.WriteLine($"| {item.FechaOperacion.ToString("dd/MM/yyyy HH:mm")} | {item.TipoOperacion.ToString().PadRight(20)} | {item.Monto.Value.ToString("#0.00").PadRight(10)} | {item.Resultado.ToString().PadRight(20)} | {item.Saldo.Value.ToString("#0.00").PadRight(10)}");
            }

        }
        else
        {
            Console.WriteLine(ObtenerMensaje(respuesta.Resultado));
        }

    }

    private static string ObtenerMensaje(ResultadoOperacion.Resultados resultado)
    {
        switch (resultado)
        {
            case ResultadoOperacion.Resultados.OK:
                return "Operación realizada con éxito.";
              
            case ResultadoOperacion.Resultados.UsuarioInexistente:
                return "Usuario inexistente.";
             
            case ResultadoOperacion.Resultados.ClaveIncorrecta:
                return "Clave incorrecta.";
                
            case ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion:
                return "No cumple con las políticas de extracción.";
               
            case ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion2:
                return "No cumple con las políticas de extracción adicionales.";
             
            case ResultadoOperacion.Resultados.SaldoInsuficiente:
                return "Saldo en su cuenta insuficiente.";
               
            case ResultadoOperacion.Resultados.SaldoCajeroInsuficiente:
                return "Saldo del cajero insuficiente.";
               
            case ResultadoOperacion.Resultados.ErrorNoControlado:
                return "Error no controlado.";
                
            case ResultadoOperacion.Resultados.UsuarioYaExistente:
                return "El usuario ya existe.";
             
            case ResultadoOperacion.Resultados.LimiteUsuariosAlcanzado:
                return "Límite de usuarios alcanzados.";
               
            case ResultadoOperacion.Resultados.NoCumpleRequisitosClave1:
                return "No cumple con los requisitos para la clave.";
  
            case ResultadoOperacion.Resultados.NoCumpleRequisitosClave2:
                return "No cumple con los requisitos adicionales para la clave.";

            default:
                return resultado.ToString();

        }
    }
}
