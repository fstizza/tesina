using System.Collections.Generic;

namespace Solucion;

public interface IEstadoUsuarios
{
    IDictionary<int, Usuario> Usuarios { get; }
}
