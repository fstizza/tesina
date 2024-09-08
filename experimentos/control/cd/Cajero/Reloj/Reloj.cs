using System;

namespace Solucion;

public class Reloj : IReloj
{
    public DateTime FechaActual => DateTime.Now;
}
