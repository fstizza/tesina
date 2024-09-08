using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;

namespace Solucion;

public class DominioRep
{
    static bool EnTransaccion = false;

    public static ResultadoOperacion Existe(Tipos tipo, int id)
    {
        if (!File.Exists(NombreArchivo(tipo, id)))
        {
            return new ResultadoOperacion(CodigosError.NoExiste, $"No existe {tipo} con Id:{id}");
        }
        return new ResultadoOperacion();
    }

    public static ResultadoOperacion ExisteAdministrador()
    {
        string adm = NombreArchivoAdministrador();
        if (string.IsNullOrEmpty(adm)) return new ResultadoOperacion(CodigosError.NoExiste, "No existe el usuario Administrador, debe inicializar el cajero");
        return new ResultadoOperacion();
    }

    public static ResultadoOperacionLeer<T> Leer<T>(Tipos tipo, int id) where T : Dominio
    {
        ResultadoOperacion ope = Existe(tipo, id);
        if (!ope.OK) return new ResultadoOperacionLeer<T>(CodigosError.NoExiste, ope.Mensaje);

        string s;
        try
        {
            FileStream ms = new FileStream(NombreArchivo(tipo, id), FileMode.Open);

            byte[] b = new byte[ms.Length];
            ms.Read(b);
            s = Encoding.Default.GetString(b);
            ms.Close();
        }
        catch (Exception ex)
        {
            return new ResultadoOperacionLeer<T>(CodigosError.NoDefinido, $"Error al leer el archivo {NombreArchivo(tipo, id)} - {ex.Message}");
        }

        Dominio o;
        switch (tipo)
        {
            case Tipos.Persona:
                o = JsonSerializer.Deserialize<Persona>(s);
                return new ResultadoOperacionLeer<T>((T)o);

            case Tipos.Cajero:
                o = JsonSerializer.Deserialize<Cajero>(s);
                return new ResultadoOperacionLeer<T>((T)o);

            case Tipos.Administrador:
                o = JsonSerializer.Deserialize<Administrador>(s);
                return new ResultadoOperacionLeer<T>((T)o);
        }
        return new ResultadoOperacionLeer<T>(CodigosError.NoDefinido, $"Error de sistema (no codificado) al leer el archivo {NombreArchivo(tipo, id)}");
    }

    public static ResultadoOperacionLeer<T> LeerAdministrador<T>() where T : Administrador
    {
        ResultadoOperacion opExiste = ExisteAdministrador();
        if (!opExiste.OK) return new ResultadoOperacionLeer<T>(opExiste);

        string s;
        try
        {
            FileStream ms = new FileStream(NombreArchivoAdministrador(), FileMode.Open);

            byte[] b = new byte[ms.Length];
            ms.Read(b);
            s = Encoding.Default.GetString(b);
            ms.Close();
        }
        catch (Exception ex)
        {
            return new ResultadoOperacionLeer<T>(CodigosError.NoDefinido, $"Error al leer el archivo {NombreArchivoAdministrador()} - {ex.Message}");
        }

        Administrador o;
        try
        {
            o = JsonSerializer.Deserialize<Administrador>(s);
            return new ResultadoOperacionLeer<T>((T)o);
        }
        catch (Exception ex)
        {
            return new ResultadoOperacionLeer<T>(CodigosError.NoDefinido, $"Error de sistema (no codificado) al leer el archivo {NombreArchivoAdministrador()} - {ex.Message}");
        }
    }


    public static ResultadoOperacion Guardar(Dominio obj)
    {
        string jsonString = null;
        string nombreArchivo = null;
        switch (obj.Tipo)
        {
            case Tipos.Persona:
                jsonString = JsonSerializer.Serialize((Persona)obj);
                nombreArchivo = NombreArchivo(obj);
                break;

            case Tipos.Cajero:
                jsonString = JsonSerializer.Serialize((Cajero)obj);
                nombreArchivo = NombreArchivo(obj);
                break;

            case Tipos.Administrador:
                jsonString = JsonSerializer.Serialize((Administrador)obj);
                nombreArchivo = NombreArchivo(obj);
                break;
        }

        if (!string.IsNullOrEmpty(jsonString))
        {
            try
            {
                if (EnTransaccion)
                {
                    string archivoBak = Path.ChangeExtension(Path.GetFileName(nombreArchivo), ".bakJson");

                    File.Copy(nombreArchivo, archivoBak, true);
                }
                File.WriteAllText(nombreArchivo, jsonString);
            }
            catch (Exception ex)
            {
                return new ResultadoOperacion(CodigosError.ErrorDePersistencia, $"Se ha producido un error al persistir {nombreArchivo} - {ex.Message}");
            }
            return new ResultadoOperacion();
        }
        else
        {
            return new ResultadoOperacion(CodigosError.ErrorDePersistencia, $"No se ha podido persistir {nombreArchivo} porque no se pudo serializar");
        }
    }

    public static string NombreArchivo(Tipos tipo, int id)
    {
        return $"{tipo}_{id:0000000000}.json";
    }
    public static string NombreArchivo(Dominio obj)
    {
        return NombreArchivo(obj.Tipo, obj.Id);
    }
    private static string NombreArchivoAdministrador()
    {
        return Directory.GetFiles("./", "Administrador_*.json").ToList().FirstOrDefault();
    }

    public static int CantidadPersonas()
    {
        int cantidad = 0;
        try
        {
            cantidad = Directory.GetFiles("./", "Persona_*.json").Count();
        }
        catch { }

        return cantidad;
    }

    #region Transaccion
    public static void BeginTran() { EnTransaccion = true; }
    public static void Commit()
    {
        foreach (string nombreArchivo in Directory.GetFiles("./", "*.bakJson"))
        {
            try
            {
                File.Delete(nombreArchivo);
            }
            catch { }
        }
        EnTransaccion = false;
    }
    public static void Rollback()
    {
        foreach (string nombreArchivo in Directory.GetFiles("./", "*.bakJson"))
        {
            string archivoJson = Path.ChangeExtension(Path.GetFileName(nombreArchivo), ".json");

            try
            {
                File.Delete(archivoJson);
                File.Move(nombreArchivo, archivoJson);
            }
            catch { }
        }
        EnTransaccion = false;
    }
    #endregion
}
