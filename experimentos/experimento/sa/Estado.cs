using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace Solucion;

public enum Operacion
{
    Extraccion = 1,
    Clave = 2
}
public enum Resultado
{
    Ok = 1,
    UsuarioInexistente,
    UsuarioYaExistente,
    ClaveIncorrecta,
    SaldoCajeroInsuficiente,
    SaldoInsuficiente,
    NoCumplePoliticaExtraccion,
    NoCumplePoliticaExtraccion2,
    UsuarioNoHabilitado,
    LimiteUsuariosAlcanzado,
    CambioDeClaveBloqueado,
    NoCumpleRequisitosClave1,
    NoCumpleRequisitosClave2
}

public interface Usuario
{
    abstract string DNI { get; set; }
    abstract string Nombre { get; set; }
    abstract string Clave { get; set; }
}

public class Administrador : Usuario
{
    string _dni = "36005591";
    string _nombre = "Ale";
    string _clave = "123456";

    public string DNI { get { return this._dni; } set { } }
    public string Nombre { get { return this._nombre; } set { } }
    public string Clave { get { return this._clave; } set { } }
}

public class Movimiento
{
    public string Tipo { get; set; }
    public DateTime Fecha { get; set; }
}

/// <summary>
/// Modelo que representa el estado del sistema.
/// </summary>
public class Estado : Usuario
{
    public static int CANT_MAX_USUARIOS = 5;
    public static int LONG_MIN_CLAVE = 8;
    public static DateTime FECHAHORA = DateTime.Now;
    public static Administrador Administrador = new Administrador();
    public float SaldoCajero { get; set; }
    public string DNI { get; set; }
    public string Nombre { get; set; }
    public string Clave { get; set; }
    public float Sueldos { get; set; }
    public float Saldo { get; set; }

    public List<Movimiento> Movimientos { get; set; }

    public Resultado UsuarioNoHabilitado(string dni, string clave)
    {
        if (Administrador.DNI.Equals(dni.Trim())) return ClaveIncorrecta(dni, clave);
        return Resultado.UsuarioNoHabilitado;
    }

    public Resultado ClaveIncorrecta(string dni, string clave)
    {
        if (Administrador.DNI.Equals(dni.Trim()) && Administrador.Clave.Equals(clave.Trim())) return Resultado.Ok;
        return Resultado.ClaveIncorrecta;
    }
    public Resultado UsuarioYaExistente(string dni)
    {

        Estado e = Cargar();
        if (e.DNI.Trim().Equals(dni.Trim())) return Resultado.UsuarioYaExistente;
        return Resultado.Ok;
    }

    public static Resultado LimiteUsuariosAlcanzado()
    {
        return Resultado.Ok;
    }

    public static Estado IniciarSesion(string dni, string clave)
    {
        Estado e = Cargar();
        if (e.DNI.Trim().Equals(dni.Trim()) && e.Clave.Trim().Equals(clave.Trim())) return e;

        return null;
    }

    public static List<Movimiento> BuscarMovimientos(string dni, DateTime desde, DateTime hasta)
    {
        Estado e = Cargar();
        if (e.DNI.Trim().Equals(dni.Trim()))
        {
            return e.Movimientos.Where(x => desde.Date <= x.Fecha.Date && x.Fecha.Date <= hasta.Date).ToList();
        }
        return null;
    }

    public static Resultado CargarSaldo(float monto)
    {
        Estado e = Cargar();

        e.SaldoCajero += monto;
        if (e.Movimientos == null)
        {
            e.Movimientos = new List<Movimiento>();
        }
        e.Movimientos.Add(new Movimiento() { Fecha = FECHAHORA, Tipo = "Depósito" });
        e.Guardar();
        return Resultado.Ok;
    }

    public static Resultado CambiarClave(string dni, string clave, string nuevaClave)
    {
        Estado e = IniciarSesion(dni, clave);
        if (e != null)
        {
            if (nuevaClave.Length < LONG_MIN_CLAVE) return Resultado.NoCumpleRequisitosClave1;
            if (!Regex.IsMatch(nuevaClave, "^[a-zA-Z0-9]*$")) return Resultado.NoCumpleRequisitosClave2;

            e.Clave = nuevaClave;
            e.Movimientos.Add(new Movimiento() { Fecha = FECHAHORA, Tipo = "Cambio de clave" });
            e.Guardar();
            return Resultado.Ok;
        }
        else
        {
            return Resultado.UsuarioInexistente;
        }
    }

    public static Resultado Extraccion(string dni, string clave, float monto)
    {
        Estado e = IniciarSesion(dni, clave);
        if (e == null) return Resultado.UsuarioInexistente;
        if (!NoCumplePoliticaExtraccion(e.Movimientos)) return Resultado.NoCumplePoliticaExtraccion;
        if (monto > e.Sueldos / 2) return Resultado.NoCumplePoliticaExtraccion2;
        if (monto > e.Saldo) return Resultado.SaldoInsuficiente;
        if (monto > e.SaldoCajero) return Resultado.SaldoCajeroInsuficiente;

        e.SaldoCajero -= monto;
        e.Saldo -= monto;
        e.Movimientos.Add(new Movimiento() { Fecha = DateTime.Now, Tipo = "Extracción" });
        e.Guardar();
        return Resultado.Ok;
    }

    public static bool NoCumplePoliticaExtraccion(List<Movimiento> movimientos)
    {
        var count = movimientos.Where(x => x.Fecha.Date == FECHAHORA.Date).Count();
        if (count > 2) return false;
        return true;
    }

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
        return new Estado()
        {
            // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
            // Propiedad1 = valor

            DNI = string.Empty,
            Nombre = string.Empty,
            Clave = string.Empty,
            Sueldos = 0,
            Movimientos = new List<Movimiento>(),
            SaldoCajero = 0,
        };
    }
}

/* --- Ejemplo de uso ---
Estado e = Estado.Cargar();
...
e.Guardar();
*/
