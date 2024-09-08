using Solucion;

namespace Operaciones;

public class Carga
{
    public static ResultadoOperacion Ejecutar(int dni, string clave, decimal saldo)
    {
        ResultadoOperacion ope = Soporte.ValidarAdministrador(dni, clave);
        if (!ope.OK) return ope;

        // Obtiene el cajero
        ResultadoOperacionLeer<Cajero> opeCajero = DominioRep.Leer<Cajero>(Tipos.Cajero, 1);
        if (!opeCajero.OK) return new ResultadoOperacion(opeCajero.CodigoError, opeCajero.Mensaje);
        Cajero cajero = opeCajero.Objeto;

        // Carga
        ope = cajero.IngresarDineroAlCajero(saldo);
        if (!ope.OK) return ope;

        // Persiste
        ope = DominioRep.Guardar(cajero);
        return ope;
    }

}