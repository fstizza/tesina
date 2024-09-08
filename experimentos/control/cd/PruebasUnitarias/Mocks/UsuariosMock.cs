namespace Solucion.PruebasUnitarias;

public class UsuariosMock : Mock<IUsuarios>
{
    private Dictionary<int, Usuario> _configuracion;

    public UsuariosMock()
    {
        _configuracion = new();

        Setup(o => o.Existe(It.IsAny<Documento>()))
           .Returns((Documento dni) => _configuracion.TryGetValue(dni.Numero, out var usuario) && usuario != null);

        Setup(o => o.Obtener(It.IsAny<Documento>()))
            .Returns((Documento dni) =>
            {
                _configuracion.TryGetValue(dni.Numero, out var usuario);
                return usuario;
            });

        Setup(o => o.AutenticarUsuario(It.IsAny<Documento>(), It.IsAny<string>()))
           .Returns((Documento dni, string clave) =>
           {
               _configuracion.TryGetValue(dni.Numero, out var usuario);
               return new ResultadoAutenticarUsuario(usuario);
           });
    }

    public void Configurar(Documento dni, Usuario usuarioAutenticado)
    {
        _configuracion[dni.Numero] = usuarioAutenticado;
    }
}
