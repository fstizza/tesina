using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading;

namespace Solucion;


/// <summary>
/// Modelo que representa el estado del sistema.
/// </summary>
public class Estado
{
    // Completar con las propiedades del estado.
    public List<Usuario> Usuarios { get; set; }
    public List<Clave> Claves { get; set; }
    public List<Saldo> Saldos { get; set; }
    public List<Sueldo> Sueldos { get; set; }
    public List<Movimiento> Movimientos { get; set; }
    public decimal Saldo { get; set; }
    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        string ruta = Path.Combine("estado.json");
        if (ruta.StartsWith("/"))
        {
            ruta = "." + ruta;
        }
        string contenido = JsonSerializer.Serialize(this);
        File.WriteAllText(ruta, contenido, Encoding.UTF8);
    }

    /// <summary>
    /// Retorna una instancia del modelo de estado con los valores guardados en `estado.json`.
    /// </summary>
    public static Estado Cargar()
    {
        string ruta = Path.Combine("estado.json");
        string contenido = "";
        if (File.Exists(ruta))
        {
            contenido = File.ReadAllText(ruta, Encoding.UTF8);
        }

        if (contenido == "")
        {
            return Inicial();
        }
        else
        {
            return JsonSerializer.Deserialize<Estado>(contenido);
        }
    }

    public static FechaHora MISMO_MES(DateTime fechaHora)
    {
        int yyyy = fechaHora.Year;
        int mm = fechaHora.Month;

        return new FechaHora()
        {
            ValorFechaHora = new DateTime(yyyy, mm, 1)
        };
    }


    public static FechaHora MISMO_DIA(DateTime fechaHora)
    {
        int yyyy = fechaHora.Year;
        int mm = fechaHora.Month;
        int dd = fechaHora.Day;

        return new FechaHora()
        {
            ValorFechaHora = new DateTime(yyyy, mm, dd)
        };
    }

    public static int DIF_FECHAS_DIAS(DateTime f1, DateTime f2)
    {
        TimeSpan diferencia = f1 - f2;

        return Math.Abs(diferencia.Days);
    }

    public static int LONGITUD(string clave)
    {
        return clave.Length;
    }


    /// <summary>
    /// Retorna una instancia del modelo de estado con sus valores iniciales.
    /// </summary>
    private static Estado Inicial()
    {
        return new Estado()
        {
            // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
            // Propiedad1 = valor
            Usuarios = new List<Usuario>()
            {
                new Usuario()
                {
                    ValorDNI = ConstantesGlobales.ADMINISTRADOR,
                    ValorNombre = ConstantesGlobales.NOMBRE
                }
            },
            Claves = new List<Clave>()
            {
                new Clave()
                {
                    ValorDNI = ConstantesGlobales.ADMINISTRADOR,
                    ValorClave = ConstantesGlobales.CLAVE,
                }
            },
            Saldos = new List<Saldo>(),
            Sueldos = new List<Sueldo>(),
            Movimientos = new List<Movimiento>()
        };

    }
}

public class ConstantesGlobales
{
    public const int CANT_MAX_USUARIOS = 5;
    public const int LONG_MIN_CLAVE = 8;
    public const string ADMINISTRADOR = "administrador";
    public const string NOMBRE = "nombre_administrador";
    public const string CLAVE = "clave_administrador";
    public DateTime AHORA = DateTime.Now;
}

public abstract class DNI
{
    public string ValorDNI { get; set; }
}

public abstract class Nombre : DNI
{
    public string ValorNombre { get; set; }
}

public class Clave : DNI
{
    public string ValorClave { get; set; }
}

public abstract class Monto : DNI
{
    public decimal ValorMonto { get; set; }
}

public class FechaHora
{
    public DateTime ValorFechaHora { get; set; }
}

public enum Operacion
{
    Extraccion,
    Clave,
}

public class Usuario : Nombre
{

}

public class Saldo : Monto
{

}

public class Sueldo : Monto
{

}

public class Movimiento : DNI
{
    public FechaHora FechaHora { get; set; }

    public Operacion Operacion { get; set; }
}
/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
