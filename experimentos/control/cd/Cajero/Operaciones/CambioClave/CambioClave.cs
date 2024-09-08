using System;

namespace Solucion;

public class CambioClave : Operacion
{
    private readonly IReloj _reloj;
    private readonly PoliticaSeguridad _politicaSeguridad;
    private readonly IUsuarios _usuarios;
    private readonly IHistorialCambiosClave _historialCambiosClave;

    public CambioClave(
        IReloj reloj,
        PoliticaSeguridad politicaSeguridad,
        IUsuarios usuarios,
        IHistorialCambiosClave historialCambiosClave) : base(usuarios)
    {
        _reloj = reloj;
        _politicaSeguridad = politicaSeguridad;
        _usuarios = usuarios;
        _historialCambiosClave = historialCambiosClave;
    }

    public ResultadoOperacion Ejecutar(SolicitudCambioClave solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        ResultadoOperacion resultado;

        var fechaActual = _reloj.FechaActual;

        if (UsuarioNoAutenticado(solicitud.Dni, solicitud.ClaveActual, out var usuario, out var codigo, out var mensaje) ||
            ExcedeCantidadCambiosDeClavePorPeriodo(usuario, fechaActual, out codigo, out mensaje) ||
            NuevaClaveNoSatisfacePolitica(solicitud.ClaveNueva, out codigo, out mensaje))
        {
            resultado = new ResultadoOperacion(false, codigo, mensaje);
        }
        else
        {
            _usuarios.CambiarClave(usuario, solicitud.ClaveNueva, fechaActual);

            resultado = new ResultadoOperacion(true, "CC00", "Su clave ha sido modificada exitosamente.");
        }

        _historialCambiosClave.RegistrarIntentoCambioClave(solicitud.Dni, fechaActual, resultado.OperacionExitosa, resultado.Mensaje);

        return resultado;
    }

    private bool ExcedeCantidadCambiosDeClavePorPeriodo(Usuario usuario, DateTime fechaActual, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;
        var excede = false;
        var politica = _politicaSeguridad.CambiosClave;

        if (politica.CantidadCambiosClaveAdmitidosPorPeriodo > 0 && politica.Periodo > TimeSpan.Zero)
        {
            var fechaDesde = fechaActual.Subtract(politica.Periodo);

            var cantidadCambiosClaveEnPeriodo = _historialCambiosClave.ObtenerCantidadCambiosClaveDesdeFecha(usuario, fechaDesde);

            excede = cantidadCambiosClaveEnPeriodo >= politica.CantidadCambiosClaveAdmitidosPorPeriodo;

            if (excede)
            {
                codigo = "CC01";
                mensaje = "No puede cambiar su clave con tanta frecuencia.";
            }
        }

        return excede;
    }

    private bool NuevaClaveNoSatisfacePolitica(string claveNueva, out string codigo, out string mensaje)
    {
        codigo = null;

        var satisface = _politicaSeguridad.ComplejidadClave.EsSatisfecha(claveNueva, out mensaje);

        if (!satisface)
        {
            codigo = "CC02";
        }

        return !satisface;
    }
}
