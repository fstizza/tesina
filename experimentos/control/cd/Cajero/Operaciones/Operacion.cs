namespace Solucion;

public abstract class Operacion
{
    private readonly IUsuarios _usuarios;

    protected Operacion(IUsuarios usuarios)
    {
        _usuarios = usuarios;
    }

    protected bool UsuarioNoAutenticado(Documento dni, string clave, out Usuario usuario, out string codigo, out string mensaje)
    {
        var autenticacionUsuario = _usuarios.AutenticarUsuario(dni, clave);

        (usuario, codigo, mensaje) = (autenticacionUsuario.Usuario, autenticacionUsuario.CodigoError, autenticacionUsuario.MensajeError);

        return autenticacionUsuario.Usuario == null;
    }

    protected static bool UsuarioNoEsAdministrador(Usuario usuario, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        if (!usuario.EsAdministrador)
        {
            codigo = "S02";
            mensaje = "Esta operación es sólo para administradores.";
        }

        return !usuario.EsAdministrador;
    }
}
