using System.Collections.Generic;

namespace Solucion
{
    public interface IEstadoMovimientos
    {
        IList<Movimiento> Movimientos { get; }
    }
}
