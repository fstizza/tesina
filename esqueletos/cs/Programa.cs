using System;
using System.Linq;

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
            case "extraccion":
                // TODO: Completar.
                break;
            case "clave":
                // TODO: Completar.
                break;
            case "saldo":
                // TODO: Completar.
                break;
            case "alta":
                // TODO: Completar.
                break;
            case "carga":
                // TODO: Completar.
                break;
            case "movimientos":
                // TODO: Completar.
                break;
            default:
                Console.WriteLine("Operación inválida.");
                System.Environment.Exit(1);
                break;
        }
    }
}
