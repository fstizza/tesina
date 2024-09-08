using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Solucion;


/// <summary>
/// Modelo que representa el estado del sistema.
/// </summary>
public class Estado
{
    // Completar con las propiedades del estado.
    public Dictionary<string, Usuario> Usuarios;
    public Dictionary<string, decimal> SaldosUsuarios;
    public List<MovimientoCaja> HistoricoMovimientos;
    public List<CambioPassword> HistoricoClaves;
    public HashSet<string> UsuariosAdmin;
    public decimal SaldoCajero;

    public Estado() { }

    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        // string ruta = Path.Combine(Directory.GetParent(Environment.CurrentDirectory).Parent.Parent.FullName, "estado.json");
        // El parent parent es solo necesario si se ejecuta desde visual studio porque compila el proyecto en la carpeta bin y lo corre desde ahi
        string ruta = Path.Combine(Environment.CurrentDirectory, "estado.json");
        if (ruta.StartsWith("/"))
        {
            ruta = "." + ruta;
        }
        var options = new JsonSerializerOptions { IncludeFields = true };
        string contenido = JsonSerializer.Serialize(this, options);

        File.WriteAllText(ruta, contenido, Encoding.UTF8);
    }

    /// <summary>
    /// Retorna una instancia del modelo de estado con los valores guardados en `estado.json`.
    /// </summary>
    public static Estado Cargar()
    {
        // string ruta = Path.Combine(Directory.GetParent(Environment.CurrentDirectory).Parent.Parent.FullName, "estado.json");
        string ruta = Path.Combine(Environment.CurrentDirectory, "estado.json");
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
            var options = new JsonSerializerOptions { IncludeFields = true };
            return JsonSerializer.Deserialize<Estado>(contenido, options);
        }
    }


    /// <summary>
    /// Retorna una instancia del modelo de estado con sus valores iniciales.
    /// </summary>
    private static Estado Inicial()
    {
        return new Estado()
        {
            Usuarios = new() { { "admin", new Usuario("admin", 1000, "admin") } },
            SaldosUsuarios = new(),
            HistoricoMovimientos = new(),
            HistoricoClaves = new(),
            UsuariosAdmin = new() { "admin" },
            SaldoCajero = 50_000
        };
    }
}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
