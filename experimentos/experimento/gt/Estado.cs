using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;

namespace Solucion;


/// <summary>
/// Modelo que representa el estado del sistema.
/// </summary>
public class Estado
{
    // Completar con las propiedades del estado.
    public Dictionary<int, string> usuarios { get; set; }
    public Dictionary<int, string> claves { get; set; }
    public Dictionary<int, int> saldos { get; set; }
    public Dictionary<int, int> sueldos { get; set; }
    public Dictionary<int, Dictionary<DateTime, OPERACION>> movimientos { get; set; }
    public int saldo { get; set; }

    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        string ruta = "C:\\Users\\fs80235\\Desktop\\atm\\experimentos\\experimento\\Galli-Tomas\\estado.json";
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
        string ruta = "C:\\Users\\fs80235\\Desktop\\atm\\experimentos\\experimento\\Galli-Tomas\\estado.json";
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

    /// <summary>
    /// Retorna una instancia del modelo de estado con sus valores iniciales.
    /// </summary>
    private static Estado Inicial()
    {
        var estado = new Estado();

        estado.usuarios = new Dictionary<int, string>
        {
            { Globales.administrador, Globales.nombre_administrador }
        };
        estado.claves = new Dictionary<int, string>
        {
            { Globales.administrador, Globales.clave_administrador }
        };
        estado.saldos = new Dictionary<int, int>();
        estado.sueldos = new Dictionary<int, int>();
        estado.movimientos = new Dictionary<int, Dictionary<DateTime, OPERACION>>();
        estado.saldo = 0;

        return estado;
    }

    public static class Globales
    {
        public readonly static int CANT_MAX_USUARIOS = 5;
        public readonly static int LONG_MIN_CLAVE = 8;
        public readonly static int administrador = 12345678;
        public readonly static string nombre_administrador = "admin";
        public readonly static string clave_administrador = "admin123";
        public static DateTime ahora => DateTime.Now;
    }
}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
