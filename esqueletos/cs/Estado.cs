using System;
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


    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        string ruta = Path.Combine(Directory.GetParent(Environment.CurrentDirectory).Parent.Parent.FullName, "estado.json");
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
        string ruta = Path.Combine(Directory.GetParent(Environment.CurrentDirectory).Parent.Parent.FullName, "estado.json");
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
        return new Estado()
        {
            // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
            // Propiedad1 = valor
        };
    }
}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
