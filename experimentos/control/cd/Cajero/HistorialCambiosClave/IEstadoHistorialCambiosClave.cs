using System.Collections.Generic;

namespace Solucion;

public interface IEstadoHistorialCambiosClave
{
    IDictionary<int, IList<RegistroCambioClave>> CambiosClave { get; }
}
