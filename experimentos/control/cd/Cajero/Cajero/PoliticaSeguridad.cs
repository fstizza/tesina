using System;
using System.Linq;

namespace Solucion;

public class PoliticaSeguridad
{
    public PoliticaSeguridad()
    {
        ComplejidadClave = new PoliticaComplejidadClave(8, true, true);
        CambiosClave = new PoliticaCambiosClave(1, TimeSpan.FromDays(30));
        CantidadMaximaUsuarios = 5;
    }

    public PoliticaComplejidadClave ComplejidadClave { get; set; }

    public PoliticaCambiosClave CambiosClave { get; set; }

    public int CantidadMaximaUsuarios { get; set; }
}

public record PoliticaComplejidadClave(
    byte LongitudMinimaClave,
    bool RequiereLetras,
    bool RequiereDigitos 
)
{
    public bool EsSatisfecha(string clave, out string motivo)
    {
        if (LongitudMinimaClave > 0 && (clave ?? "").Length < LongitudMinimaClave)
        {
            motivo = $"La clave debe tener al menos {LongitudMinimaClave} caracter{(LongitudMinimaClave > 1 ? "s" : "")}.";
            return false;
        }
        else if (RequiereLetras && !(clave ?? "").Any(c => char.IsLetter(c)))
        {
            motivo = "La clave debe tener alguna letra";
            return false;
        }
        else if (RequiereDigitos && !(clave ?? "").Any(c => char.IsDigit(c)))
        {
            motivo = "La clave debe tener algún dígito.";
            return false;
        }
        else
        {
            motivo = null;
            return true;
        }
    }
}

public record PoliticaCambiosClave
(
    int CantidadCambiosClaveAdmitidosPorPeriodo,
    TimeSpan Periodo
);
