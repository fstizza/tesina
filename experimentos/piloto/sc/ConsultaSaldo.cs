using Solucion;

namespace Operaciones;

public class ConsultaSaldo
{
    public static ResultadoOperacionSaldoEnCajero Ejecutar(int dni, string clave)
    {
        // Precondiciones
        ResultadoOperacionLeer<Persona> opePersona = Soporte.ValidarPersona<Persona>(dni, clave);
        if (!opePersona.OK) return new ResultadoOperacionSaldoEnCajero(opePersona.CodigoError,opePersona.Mensaje);

        // Consulta
        return new ResultadoOperacionSaldoEnCajero(opePersona.Objeto.Saldo);
    }
}
