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

    public IDictionary<int, Usuario> Usuarios { get; set; } 

    public IList<Movimiento> Movimientos { get; set; } 

    public decimal DineroDisponible { get; set; }

    public Dictionary<int, IList<RegistroCambioClave>> CambiosClave { get; set; }

    /// <summary>
    /// Guarda la instancia actual del modelo de Estado en el archivo `estado.json`.
    /// </summary>
    public void Guardar()
    {
        string ruta = "C:\\Users\\fs80235\\Desktop\\atm\\experimentos\\control\\Cepero-Diego\\Cajero\\estado.json";
        string contenido = JsonSerializer.Serialize(this);
        File.WriteAllText(ruta, contenido, Encoding.UTF8);
    }

    /// <summary>
    /// Retorna una instancia del modelo de estado con los valores guardados en `estado.json`.
    /// </summary>
    public static Estado Cargar()
    {
        string ruta = "C:\\Users\\fs80235\\Desktop\\atm\\experimentos\\control\\Cepero-Diego\\Cajero\\estado.json";
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
        var administrador = new Usuario()
        {
            NombreApellido = "Administrador",
            NumeroDocumento = 12345678, 
            EsAdministrador = true,
            HashClave = "adm1n1strad0r"
        };

        return new Estado()
        {
            Usuarios = new Dictionary<int, Usuario>
            {
                { administrador.NumeroDocumento, administrador },
            },
            Movimientos = new List<Movimiento>(),
            DineroDisponible = 0,
            CambiosClave = new()
        };
    }
}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
