using System;
using System.Security.Cryptography;
using System.Text;

namespace Solucion;

public class Usuarios : IUsuarios
{
    private readonly IEstadoUsuarios _estado;

    public Usuarios(IEstadoUsuarios estado)
    {
        _estado = estado;
    }

    public int Cantidad => _estado.Usuarios.Count;

    public bool Existe(Documento dni)
    {
        return _estado.Usuarios.ContainsKey(dni.Numero);
    }

    public Usuario Obtener(Documento dni)
    {
        _estado.Usuarios.TryGetValue(dni.Numero, out var usuario);

        return usuario;
    }

    public void Agregar(Usuario usuario, string clave)
    {
        var hashClave = ObtenerHashClave(clave);

        usuario.HashClave = hashClave;

        _estado.Usuarios[usuario.NumeroDocumento] = usuario;
    }

    public ResultadoAutenticarUsuario AutenticarUsuario(Documento dni, string clave)
    {
        if (_estado.Usuarios.TryGetValue(dni?.Numero ?? -1, out var usuario) && ObtenerHashClave(clave) == usuario.HashClave)
        {
            return new ResultadoAutenticarUsuario(usuario);
        }
        else
        {
            return new ResultadoAutenticarUsuario(
                Usuario: null, CodigoError: "S01", MensajeError: "Usuario inexistente o clave errónea.");
        }
    }

    public void CambiarClave(Usuario usuario, string clave, DateTime fechaActual)
    {
        usuario.HashClave = ObtenerHashClave(clave); ;
        usuario.FechaUltimoCambioClave = fechaActual;
    }

    public static string ObtenerHashClave(string clave)
    {
        return clave;
    }
}
