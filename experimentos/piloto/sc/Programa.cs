using Operaciones;
using System;

namespace Solucion;

public class Programa
{

    public static void Main()
    {
        ResultadoOperacion ope = Inicializar.Ejecutar(16066091, "Stizza, Carlos Alberto", "pirulo");
        if (!ope.OK)
        {
            Console.WriteLine(ope.Mensaje);
            Console.ReadLine();
        }

        /*
        ope = Carga.Ejecutar(16066091, "pirulo", 100000);
        if (!ope.OK)
        {
            Console.WriteLine(ope.Mensaje);
            Console.ReadLine();
        }


        ope = AltaUsuario.Ejecutar(16066091, "pirulo", 41404842, "fede", "Stizza, Federico", 50000, 75000);
        if (!ope.OK)
        {
            Console.WriteLine(ope.Mensaje);
            Console.ReadLine();
        }


        ope = Extraccion.Ejecutar(41404842, "fede", 10000);
        if (!ope.OK)
        {
            Console.WriteLine(ope.Mensaje);
            Console.ReadLine();
        }

        ope = Extraccion.Ejecutar(41404842, "fede", 18500);
        if (!ope.OK)
        {
            Console.WriteLine(ope.Mensaje);
            Console.ReadLine();
        }

        ResultadoOperacionSaldoEnCajero opeSaldoCajero = ConsultaSaldoCajero.Ejecutar(16066091, "pirulo");
        if (!opeSaldoCajero.OK)
        {
            Console.WriteLine(opeSaldoCajero.Mensaje);
        }
        else
        {
            Console.WriteLine($"Saldo del cajero: {opeSaldoCajero.Saldo:C2}");
        }
        Console.ReadLine();

        ResultadoOperacionSaldoEnCajero opeSaldoPersona = ConsultaSaldo.Ejecutar(41404842, "fede");
        if (!opeSaldoPersona.OK)
        {
            Console.WriteLine(opeSaldoPersona.Mensaje);
        }
        else
        {
            Console.WriteLine($"Saldo del cajero: {opeSaldoPersona.Saldo:C2}");
        }
        Console.ReadLine();
        */

        ResultadoOperacion opeAdelanto = Adelanto.Ejecutar(41404842, "fede", 25000);
        if (!opeAdelanto.OK)
        {
            Console.WriteLine(opeAdelanto.Mensaje);
        }

        ResultadoOperacionMovimientoDelUsuario opeMov = ConsultaMovimientos.Ejecutar(16066091, "pirulo", 41404842, new DateTime(2023, 07, 13, 10, 0, 0), new DateTime(2023, 07, 14, 23, 0, 0));
        if (!opeMov.OK)
        {
            Console.WriteLine(opeMov.Mensaje);
        }
        else
        {
            Console.WriteLine("Lista de movimientos");
            foreach (Movimiento mov in opeMov.Movimientos)
            {
                Console.WriteLine($"  {mov.Fecha:dd/MM/yyyy HH:mm:ss} - {mov.Descripcion}");
            }
        }

        ResultadoOperacionSaldoEnCajero opeSaldoPersona = ConsultaSaldo.Ejecutar(41404842, "fede");
        if (!opeSaldoPersona.OK)
        {
            Console.WriteLine(opeSaldoPersona.Mensaje);
        }
        else
        {
            Console.WriteLine($"Saldo del cajero: {opeSaldoPersona.Saldo:C2}");
        }
        Console.ReadLine();


        // Punto de entrada del proyecto, util para llamar a los scripts individuales...
        // Adelanto.Ejecutar(), AltaUsuario.Ejecutar(), ...

        System.Environment.Exit(7);
    }

    public static Cajero Cajero { get; private set; }

}