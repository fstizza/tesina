using System;
using System.Collections.Generic;
using System.Linq;

namespace Solucion;

public class Persona : Dominio
{
    public Persona(int dni, string apellidoYNombres, string clave, decimal sueldo, decimal saldo) : base(Tipos.Persona, dni)
    {
        ApellidoYNombres = apellidoYNombres;
        Sueldo = sueldo;
        Saldo = saldo;
        Clave = clave;
    }

    #region Propiedades

    public int DNI => Id;
    public string ApellidoYNombres { get; set; }
    public string Clave { get; set; }
    public DateTime? UltimoCambioDeClave { get; set; }
    public decimal Sueldo { get; set; }
    public decimal Saldo { get; set; }
    public Dictionary<DateTime, decimal> Extracciones { get; set; } = new Dictionary<DateTime, decimal>();
    public Dictionary<DateTime, decimal> Adelantos { get; set; } = new Dictionary<DateTime, decimal>();

    #endregion

    #region Operaciones

    public ResultadoOperacion ValidarClave(string clave) 
    { 
        if (clave != Clave)
        {
            return new ResultadoOperacion(CodigosError.UsuarioOClaveIncorrecto, "El DNI o la clave son incorrectos");
        }
        return new ResultadoOperacion();
    }

    public ResultadoOperacion Extraer(decimal importe)
    {
        // Precondiciones
        ResultadoOperacion ope = PuedeExtraer(importe);
        if (!ope.OK) return ope;

        // Extracción
        Saldo -= importe;
        Extracciones.Add(DateTime.Now, importe);
        Movimientos.Add(new Movimiento($"Extracción de {importe:C2}"));

        return ope;
    }


    #endregion

    #region Precondiciones

    public ResultadoOperacion PuedeExtraer(decimal importe)
    {
        // Verificaciones
        if (importe <= 0) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor de la extracción deber ser mayor que cero. Se ha recibido {importe:C2}");
        if (importe > Sueldo / 2) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor de la extración no puede superar a la mitad del sueldo. Se ha recibido {importe:C2}");
        if (Extracciones.Count(e => e.Key.Date == DateTime.Now.Date) == 2) return new ResultadoOperacion(CodigosError.TopeExtraccionesDiarias, "Sólo se permiten 2 extracciones diarias");
        if (Saldo < importe) return new ResultadoOperacion(CodigosError.SaldoInsuficiente, $"El valor de la extracción supera el saldo de la cuenta. Se ha recibido {importe:C2}");
        return new ResultadoOperacion();
    }

    public ResultadoOperacion PuedeSolicitarAdelanto(decimal importe)
    {
        // Verificaciones
        if (importe <= 0) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor del adelanto deber ser mayor que cero. Se ha recibido {importe:C2}");
        if (importe > Sueldo / 2) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor del adelanto no puede superar a la mitad del sueldo. Se ha recibido {importe:C2}");
        if (Adelantos.Any(e => e.Key.Date == DateTime.Now.Date)) return new ResultadoOperacion(CodigosError.TopeExtraccionesDiarias, "Sólo se permite solicitar un adelanto por mes");
        return new ResultadoOperacion();
    }
    #endregion
}
