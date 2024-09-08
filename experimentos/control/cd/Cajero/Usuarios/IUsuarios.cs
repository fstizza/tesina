using System;

namespace Solucion;

public interface IUsuarios
{
    int Cantidad { get; }

    bool Existe(Documento dni);

    Usuario Obtener(Documento dni);

    void Agregar(Usuario usuario, string clave);

    ResultadoAutenticarUsuario AutenticarUsuario(Documento dni, string clave);

    void CambiarClave(Usuario usuario, string clave, DateTime fechaActual);
}
