using System;
using System.Collections.Generic;
using System.Linq;

namespace Solucion;

public class HistorialCambiosClave : IHistorialCambiosClave
{
    private readonly IEstadoHistorialCambiosClave _estado;

    public HistorialCambiosClave(IEstadoHistorialCambiosClave estado)
    {
        _estado = estado;
    }

    public int ObtenerCantidadCambiosClaveDesdeFecha(Usuario usuario, DateTime fechaDesde)
    {
        if (!_estado.CambiosClave.TryGetValue(usuario.NumeroDocumento, out var cambiosClave))
        {
            return 0;
        }
        else
        {
            return cambiosClave.Count(o => o.Exitoso && o.Fecha >= fechaDesde);
        }
    }

    public RegistroCambioClave RegistrarIntentoCambioClave(Documento dni, DateTime fecha, bool exitoso, string motivo)
    {
        var registro = new RegistroCambioClave(dni, fecha, exitoso, (exitoso ? null: motivo));

        if (!_estado.CambiosClave.TryGetValue(dni, out var historial))
        {
            historial = new List<RegistroCambioClave>();
            _estado.CambiosClave.Add(dni, historial);
        }

        historial.Add(registro);

        return registro;
    }
}
