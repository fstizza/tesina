using System;
using System.Collections.Generic;
using System.Linq;

namespace Solucion;

public class Programa
{
    public static void Main(string[] args)
    {
        //args = new string[4] { "carga", "12345678", "admin123", "40000" };
        //args = new string[7] { "alta", "12345678", "admin123", "34858394", "clave123","Juan2", "38000" };
        //args = new string[4] { "extraccion", "34858394", "clave123", "300"};
        //args = new string[3] { "saldo", "34858394", "clave123"};
        //args = new string[4] { "clave", "34858394", "clave123", "clave1234"};
        //args = new string[6] { "movimientos", "12345678", "admin123", "34858394", "25/4/1990 20:10:15", "22/8/2023 21:10:15" };

        if (!args.Any())
        {
            Console.WriteLine("Sin argumentos.");
            System.Environment.Exit(1);
        }

        var estado = Estado.Cargar();

        var movimientos = new List<(DateTime, OPERACION)>();
        RESULTADO resultado = RESULTADO.ok;
        int saldo = 0;

        switch (args[0])
        {
            case "extraccion":
                resultado = Suboperaciones.Extraccion(estado, int.Parse(args[1]), args[2], int.Parse(args[3]));

                if (resultado == RESULTADO.ok)
                {
                    Console.WriteLine("Extracción ok");
                    estado.Guardar();
                }
                else
                    Console.WriteLine("Error al extraer: " + resultado.ToString());

                break;
            case "clave":
                resultado = Suboperaciones.CambioClave(estado, int.Parse(args[1]), args[2], args[3]);

                if (resultado == RESULTADO.ok) {
                    Console.WriteLine("Cambio de clave ok");
                    estado.Guardar();
                }
                else
                    Console.WriteLine("Error al cambiar la clave: " + resultado.ToString());

                break;
            case "saldo":
                (resultado, saldo) = Suboperaciones.ConsultaSaldo(estado, int.Parse(args[1]), args[2]);

                if (resultado == RESULTADO.ok) {
                    Console.WriteLine("Consulta de saldo ok. El saldo es: " + saldo.ToString());
                }
                else
                    Console.WriteLine("Error al consultar el saldo: " + resultado.ToString());

                break;
            case "alta":
                resultado = Suboperaciones.AltaUsuario(estado, int.Parse(args[1]), args[2], int.Parse(args[3]), args[4], args[5], int.Parse(args[6]));

                if (resultado == RESULTADO.ok) {
                    Console.WriteLine("Alta ok");
                    estado.Guardar();
                }
                else
                    Console.WriteLine("Error al dar de alta: " + resultado.ToString());

                break;
            case "carga":
                resultado = Suboperaciones.Carga(estado, int.Parse(args[1]), args[2], int.Parse(args[3]));

                if (resultado == RESULTADO.ok) {
                    Console.WriteLine("Carga de saldo ok");
                    estado.Guardar();
                }
                else
                    Console.WriteLine("Error al cargar saldo: " + resultado.ToString());

                break;
            case "movimientos":
                (resultado, movimientos) = Suboperaciones.ConsultaMovimientos(estado, int.Parse(args[1]), args[2], int.Parse(args[3]), DateTime.Parse(args[4]),
                    DateTime.Parse(args[5]));

                if (resultado == RESULTADO.ok)
                {
                    Console.WriteLine("Consulta de movimientos ok. Movimientos: ");

                    foreach (var movimiento in movimientos)
                        Console.WriteLine("Fecha: " + movimiento.Item1.ToString() + "|  Operación: " + movimiento.Item2.ToString());

                    if (movimientos == null || movimientos.Count == 0)
                        Console.WriteLine("No hay movimientos.");
                }
                else
                    Console.WriteLine("Error al consultar movimientos: " + resultado.ToString());

                break;
            default:
                Console.WriteLine("Operación inválida.");
                System.Environment.Exit(1);
                break;
        }
    }
}
