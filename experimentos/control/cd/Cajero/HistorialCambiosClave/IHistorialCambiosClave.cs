using System;

namespace Solucion;

public interface IHistorialCambiosClave
{
    RegistroCambioClave RegistrarIntentoCambioClave(Documento dni, DateTime fecha, bool exitoso, string motivo);

    int ObtenerCantidadCambiosClaveDesdeFecha(Usuario usuario, DateTime fechaDesde);
}
