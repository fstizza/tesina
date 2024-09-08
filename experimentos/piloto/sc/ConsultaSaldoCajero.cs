using Solucion;

namespace Operaciones;

public class ConsultaSaldoCajero
{
    public static ResultadoOperacionSaldoEnCajero Ejecutar(int dni, string clave)
    {
        ResultadoOperacion ope = Soporte.ValidarAdministrador(dni, clave);
        if (!ope.OK) return new ResultadoOperacionSaldoEnCajero( ope.CodigoError,ope.Mensaje);

        // Obtiene el cajero
        ResultadoOperacionLeer<Cajero> opeCajero = DominioRep.Leer<Cajero>(Tipos.Cajero, 1);
        if (!opeCajero.OK) return new ResultadoOperacionSaldoEnCajero(opeCajero.CodigoError, opeCajero.Mensaje);
        Cajero cajero = opeCajero.Objeto;

        // Consulta
        return new ResultadoOperacionSaldoEnCajero(cajero.Saldo);
    }
}
