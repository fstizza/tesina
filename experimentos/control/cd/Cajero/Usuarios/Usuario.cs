using System;

namespace Solucion;

public class Usuario
{
    public string NombreApellido { get; init; }

    public int NumeroDocumento { get; init; }

    public decimal SueldoMensual { get; init; }

    public string HashClave { get; set; }

    public DateTime? FechaUltimoCambioClave { get; set; }

    public bool EsAdministrador { get; init; }
}