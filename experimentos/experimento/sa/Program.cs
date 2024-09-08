using Solucion;
using System;
using System.Linq;
using System.Net;
using System.Threading;

namespace Program;

public class Program
{
    public static void Main(string[] args)
    {
        //args = new string[]
        //{
        //    "alta", "36005591", "123456", "41404842", "prueba123", "Federico", "10000", "10000"
        //};

        var op = args[0];

        switch (op)
        {
            case "extraccion":
                Extraccion(args);
                break;
            case "clave":
                CambioClave(args);
                break;
            case "saldo":
                Saldo(args);
                break;
            case "alta":
                AltaUsuario(args);
                break;
            case "carga":
                CargaSaldo(args);
                break;
            case "movimientos":
                ConsultaMovimientos(args);
                break;
            default:
                Console.WriteLine("Operación inválida.");
                System.Environment.Exit(1);
                break;

        }

        //Console.WriteLine(rta);
    }

    static void AltaUsuario(string[] args)
    {
        try
        {
            Console.Write("DNI Administrador: "); var adminDni = args[1];
            Console.Write("Clave Administrador: "); var adminClave = args[2];
            Console.Write("DNI: "); var dni = args[3];
            Console.Write("Clave: "); var clave = args[4];
            Console.Write("Nombre: "); var nombre = args[5];
            Console.Write("Sueldo: "); var sueldo = float.Parse(args[6]);

            Estado e = Estado.Cargar();

            var r = e.UsuarioNoHabilitado(adminDni, adminClave);

            if (Resultado.Ok == r)
            {
                r = e.UsuarioYaExistente(dni);

                if (Resultado.Ok == r)
                {
                    Estado e2 = new Estado()
                    {
                        SaldoCajero = e.SaldoCajero,
                        Sueldos = sueldo,
                        Saldo = sueldo,
                        Nombre = nombre,
                        Clave = clave,
                        DNI = dni,
                        Movimientos = new List<Movimiento>() { new Movimiento() { Tipo = "Alta", Fecha = DateTime.Now } }
                    };
                    e2.Guardar();
                    Console.WriteLine(Resultado.Ok);
                }
            }
            Console.WriteLine(r);
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    //static Resultado Extraccion(string dni, string clave, float monto)
    static void Saldo(string[] args)
    {
        Console.Write("DNI: ");
        var dni = args[1];
        Console.Write("Clave: ");
        var clave = args[2];

        var e = Estado.IniciarSesion(dni, clave);

        if (e == null) Console.WriteLine(Resultado.UsuarioInexistente);

        Console.WriteLine("Saldo: " + e?.Saldo);
    }

    static void ConsultaMovimientos(string[] args)
    {
        Console.Write("DNI Admin: ");
        var dniAdmin = args[1];
        Console.Write("Clave Admin: ");
        var claveAdmin = args[2];
        Console.Write("DNI: ");
        var dni = args[3];
        Console.Write("Fecha desde: ");
        var fechaDesde = DateTime.Parse(args[4]);
        Console.Write("Fecha hasta: ");
        var fechaHasta = DateTime.Parse(args[5]);

        Estado e = new Estado();
        var r = e.UsuarioNoHabilitado(dniAdmin, claveAdmin);
        if (r == Resultado.Ok)
        {
            List<Movimiento> consulta = Estado.BuscarMovimientos(dni, fechaDesde, fechaHasta);
            if (consulta != null)
            {
                if (consulta.Count > 0)
                {
                    foreach (var m in consulta)
                    {
                        Console.WriteLine($"{m.Fecha}|{m.Tipo}");
                    }
                }
                else
                {
                    Console.WriteLine("Sin Movimientos");
                }
            }
            else
            {
                Console.WriteLine(Resultado.UsuarioInexistente);
            }
        }
        else Console.WriteLine(r);

    }
    static void Extraccion(string[] args)
    {
        Console.Write("DNI: ");
        var dni = args[1];
        Console.Write("Clave: ");
        var clave = args[2];
        Console.Write("Monto: ");
        var monto = float.Parse(args[3]);

        Console.WriteLine(Estado.Extraccion(dni, clave, monto));
    }

    static void CargaSaldo(string[] args)
    {
        Console.Write("DNI Admin: ");
        var dniAdmin = args[1];
        Console.Write("Clave Admin: ");
        var claveAdmin = args[2];
        Console.Write("saldo: ");

        var saldo = float.Parse(args[3]);

        Estado e = new Estado();
        var r = e.UsuarioNoHabilitado(dniAdmin, claveAdmin);
        if (r == Resultado.Ok)
        {
            Console.WriteLine(Estado.CargarSaldo(saldo));
        }
        Console.Write(r);
    }

    static void CambioClave(string[] args)
    {
        Console.Write("DNI: ");
        var dni = args[1];
        Console.Write("Clave: ");
        var clave = args[2];
        Console.Write("Nueva Clave: ");
        var nuevaClave = args[3];

        Console.Write(Estado.CambiarClave(dni, clave, nuevaClave));
    }
}
