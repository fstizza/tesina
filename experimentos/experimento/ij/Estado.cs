using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using static Solucion.ResultadoOperacion;

namespace Solucion;


/// <summary>
/// Modelo que representa el estado del sistema.
/// </summary>
public class Estado
{
    public List<Usuario> Usuarios { get; set; } = new List<Usuario>();

    [JsonIgnore]
    public Usuario UsuarioActual { get; private set; }

    public decimal Saldo { get; set; }

    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        string ruta = "estado.json";
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
        string ruta = "estado.json";
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
        Estado estado = new();
        Usuario usuario = new()
        {
            DNI = 1,
            Nombre = "Administrador",
            Clave = "admin"
        };

        estado.Usuarios.Add(usuario);
        estado.Saldo = 0;

        return estado;
    }


    public void Seleccionar(int DNI)
    {
        UsuarioActual = Usuarios.Where(u => u.DNI == DNI).FirstOrDefault();
    }

}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/


public class Usuario
{
    public int DNI { get; set; }
    public string Nombre { get; set; }
    public string Clave { get; set; }
    public decimal Saldo { get; set; }
    public decimal Sueldo { get; set; }
    public List<Operacion> Operaciones { get; set; } = new List<Operacion>();
}

public class Operacion
{
    public enum TiposOperacion
    {
        Alta,
        Carga,
        Extraccion,
        Saldo,
        CambioClave,
        ConsultaMovimientos,
    }

    public DateTime FechaOperacion { get; set; }
    public TiposOperacion TipoOperacion { get; set; }
    public Resultados Resultado { get; set; }
    public decimal? Monto { get; set; }
    public decimal? Saldo { get; set; }




}