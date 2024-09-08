using Solucion;

namespace Operaciones;

public class Extraccion
{
    public static ResultadoOperacion Ejecutar(int dni, string clave, decimal monto)
    {
        ResultadoOperacion ope;

        // Obtiene la persona
        ResultadoOperacionLeer<Persona> opeLeerPersona = DominioRep.Leer<Persona>(Tipos.Persona, dni);
        if (!opeLeerPersona.OK) return new ResultadoOperacion(opeLeerPersona.CodigoError, opeLeerPersona.Mensaje);

        Persona persona = opeLeerPersona.Objeto;
        ope = persona.ValidarClave(clave);
        if (!ope.OK) return ope;

        // Precondiciones
        ope = persona.PuedeExtraer(monto);
        if (!ope.OK) return ope;

        // Obtiene el cajero
        ResultadoOperacionLeer<Cajero> opeCajero = DominioRep.Leer<Cajero>(Tipos.Cajero, 1);
        if (!opeCajero.OK) return new ResultadoOperacion(opeCajero.CodigoError, opeCajero.Mensaje);
        Cajero cajero = opeCajero.Objeto;

        ope = cajero.PuedeExtraer(monto);
        if (!ope.OK) return ope;

        // Extracción
        ope = persona.Extraer(monto);
        if (!ope.OK) return ope;

        ope = cajero.Extraer(persona.ApellidoYNombres, monto);
        if (!ope.OK) return ope;

        // Persistencia
        DominioRep.BeginTran();
        ope = DominioRep.Guardar(persona);
        if (!ope.OK)
        {
            DominioRep.Rollback();
            return ope;
        }
        ope = DominioRep.Guardar(cajero);
        if (!ope.OK)
        {
            DominioRep.Rollback();
            return ope;
        }
        DominioRep.Commit();
        return ope;
    }
}
