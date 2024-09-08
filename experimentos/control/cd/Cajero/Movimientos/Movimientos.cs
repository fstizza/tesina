using System;
using System.Collections.Generic;
using System.Linq;

namespace Solucion;

public class Movimientos : IMovimientos
{
    private readonly IReloj _reloj;
    private readonly IEstadoMovimientos _estado;

    public Movimientos(
        IReloj reloj,
        IEstadoMovimientos estado)
    {
        _reloj = reloj;
        _estado = estado;
    }

    public int ObtenerCantidadExtraccionesPorFecha(Usuario usuario, DateOnly fecha)
    {
        return _estado.Movimientos
            .Count(o => o.Tipo == TiposMovimiento.Extraccion &&
                        o.NumeroDocumentoTitular == usuario.NumeroDocumento);
    }

    public IEnumerable<Movimiento> ObtenerMovimientosPorFecha(Usuario usuario, DateOnly fechaDesde, DateOnly fechaHasta)
    {
        return _estado.Movimientos
           .Where(o =>
           {
               var fecha = DateOnly.FromDateTime(o.Fecha);
               return o.NumeroDocumentoTitular == usuario.NumeroDocumento &&
                      fecha >= fechaDesde && fecha <= fechaHasta;
           })                           
           .OrderBy(o => o.Fecha);
    }

    public decimal ObtenerSaldoActualCuenta(Usuario usuario)
    {
        return _estado.Movimientos
            .Where(o => o.NumeroDocumentoTitular == usuario.NumeroDocumento)
            .Sum(o => o.Importe);
    }

    public Movimiento RegistrarExtraccion(Usuario usuario, ImportePositivo importe)
    {
        var extraccion = new Movimiento
        (
            NumeroDocumentoTitular: usuario.NumeroDocumento,
            Fecha: _reloj.FechaActual,
            Tipo: TiposMovimiento.Extraccion,
            Importe: -importe
        );

        _estado.Movimientos.Add(extraccion);

        return extraccion;
    }

    public Movimiento RegistrarSaldoInicial(Usuario usuario, ImportePositivo importe)
    {
        var saldoInicial = new Movimiento
        (
            NumeroDocumentoTitular: usuario.NumeroDocumento,
            Fecha: _reloj.FechaActual,
            Tipo: TiposMovimiento.SaldoInicial,
            Importe: importe
        );

        _estado.Movimientos.Add(saldoInicial);

        return saldoInicial;
    }
}
