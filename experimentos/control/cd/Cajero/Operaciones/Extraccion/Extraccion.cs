using System;

namespace Solucion;

public class Extraccion : Operacion
{
    private readonly IReloj _reloj;
    private readonly PoliticaExtracciones _politicaExtracciones;
    private readonly IMovimientos _movimientos;
    private readonly IGestionDinero _gestionDinero;

    public Extraccion(
        IReloj reloj,
        PoliticaExtracciones politicaExtracciones,
        IUsuarios usuarios,
        IMovimientos movimientos,
        IGestionDinero gestionDinero) : base(usuarios)
    {
        _reloj = reloj;
        _politicaExtracciones = politicaExtracciones;
        _movimientos = movimientos;
        _gestionDinero = gestionDinero;
    }

    public ResultadoExtraccion Ejecutar(SolicitudExtraccion solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        if (UsuarioNoAutenticado(solicitud.Dni, solicitud.Clave, out var usuario, out var codigo, out var mensaje) ||
            ExcedeCantidadExtraccionesDiarias(usuario, out codigo, out mensaje) ||
            ExcedeImporteMaximoPorExtraccion(usuario, solicitud.Monto, out codigo, out mensaje) ||
            ExcedeSaldoCuenta(usuario, solicitud.Monto, out codigo, out mensaje) ||
            DineroInsuficienteEnCajero(solicitud.Monto, out codigo, out mensaje))
        {
            return new ResultadoExtraccion(false, codigo, mensaje);
        }
        else
        {
            _movimientos.RegistrarExtraccion(usuario, solicitud.Monto);
            _gestionDinero.Entregar(solicitud.Monto);

            return new ResultadoExtraccion(true, "EX00", "Retire su dinero");
        }
    }

    private bool ExcedeCantidadExtraccionesDiarias(Usuario usuario, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;
        var excede = false;

        if (_politicaExtracciones.CantidadMaximaExtraccionesDiarias > 0)
        {
            var hoy = DateOnly.FromDateTime(_reloj.FechaActual);

            var cantidadExtraccionesHoy = _movimientos.ObtenerCantidadExtraccionesPorFecha(usuario, hoy);

            excede = cantidadExtraccionesHoy + 1 > _politicaExtracciones.CantidadMaximaExtraccionesDiarias;

            if (excede)
            {
                codigo = "EX01";
                var cantidad = _politicaExtracciones.CantidadMaximaExtraccionesDiarias;
                mensaje = $"Sólo puede realizar {cantidad} extracci{(cantidad == 1 ? "ón": "ones")} por día.";
            }
        }

        return excede;
    }

    private bool ExcedeImporteMaximoPorExtraccion(Usuario usuario, ImportePositivo importe, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;
        var excede = false;

        if (_politicaExtracciones.PorcentajeDelSalarioMaximoPorExtraccion > 0)
        {
            var importeMaximoPorExtraccion = usuario.SueldoMensual * _politicaExtracciones.PorcentajeDelSalarioMaximoPorExtraccion / 100;

            excede = importe.Valor > importeMaximoPorExtraccion;

            if (excede)
            {
                codigo = "EX02";
                mensaje = "Excede el importe máximo por extracción.";
            }
        }

        return excede;
    }

    private bool ExcedeSaldoCuenta(Usuario usuario, ImportePositivo importe, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        var saldoCuenta = _movimientos.ObtenerSaldoActualCuenta(usuario);

        var excede = importe > saldoCuenta;

        if (excede)
        {
            codigo = "EX03";
            mensaje = "Excede el saldo de su cuenta.";
        }

        return excede;
    }

    private bool DineroInsuficienteEnCajero(ImportePositivo importe, out string codigo, out string mensaje)
    {
        var resultado = _gestionDinero.ValidarDisponibilidadDinero(importe);

        codigo = resultado.Codigo;
        mensaje = resultado.MensajeError;

        return !resultado.Disponible;
    }
}