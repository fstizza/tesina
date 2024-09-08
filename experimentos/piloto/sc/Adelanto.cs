using Solucion;
using System;
using System.Linq;

namespace Operaciones;
public class Adelanto
{
    public static ResultadoOperacion Ejecutar(int dni, string clave, decimal monto)
    {
        // Precondiciones
        ResultadoOperacionLeer<Persona> opePersona = Soporte.ValidarPersona<Persona>(dni, clave);
        if (!opePersona.OK) return new ResultadoOperacionSaldoEnCajero(opePersona.CodigoError, opePersona.Mensaje);

        Persona persona = opePersona.Objeto;

        if (monto <= 0) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El monto para el adelanto debe ser mayor que cero");
        if (monto > persona.Sueldo / 2) new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El monto para el adelanto supera la mitad del sueldo");
        if (persona.Adelantos.Any(a => a.Key.ToString("yyyyMM") == DateTime.Now.ToString("yyyyMM"))) return new ResultadoOperacion(CodigosError.TopeAdelantosMensual, "Sólo se permite un adelanto de sueldo al mes");

        persona.Adelantos.Add(DateTime.Now, monto);
        persona.Movimientos.Add(new Movimiento($"Adelanto de sueldo de {monto:C2}"));
        persona.Saldo += monto;

        return DominioRep.Guardar(persona);
    }
}
