using System;
using System.Collections.Generic;

namespace Solucion
{
    public interface IMovimientos
    {
        int ObtenerCantidadExtraccionesPorFecha(Usuario usuario, DateOnly fecha);

        decimal ObtenerSaldoActualCuenta(Usuario usuario);

        Movimiento RegistrarExtraccion(Usuario usuario, ImportePositivo importe);

        Movimiento RegistrarSaldoInicial(Usuario usuario, ImportePositivo importe);

        IEnumerable<Movimiento> ObtenerMovimientosPorFecha(Usuario usuario, DateOnly fechaDesde, DateOnly fechaHasta);
    }
}
