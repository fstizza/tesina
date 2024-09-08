using System;

namespace Solucion;

public class Movimiento
{
    public Movimiento(string descripcion)
    {
        Fecha = DateTime.Now;
        Descripcion = descripcion;
    }
    public DateTime Fecha { get; set; }
    public string Descripcion { get; set; }
}
