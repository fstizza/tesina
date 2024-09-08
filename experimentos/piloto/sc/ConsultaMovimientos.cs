using Solucion;
using System;
using System.Linq;

namespace Operaciones;

public class ConsultaMovimientos
{
    // TODO: Utilizar los tipos que correspondan.
    public static ResultadoOperacionMovimientoDelUsuario Ejecutar(int dni, string clave, int dni_consulta, DateTime desde, DateTime hasta)
    {
        ResultadoOperacion ope = Soporte.ValidarAdministrador(dni, clave);
        if (!ope.OK) return new ResultadoOperacionMovimientoDelUsuario(ope);

        ResultadoOperacionLeer<Persona> opePersona = DominioRep.Leer<Persona>(Tipos.Persona, dni_consulta);
        if (!opePersona.OK) return new ResultadoOperacionMovimientoDelUsuario(opePersona.CodigoError, opePersona.Mensaje);

        Persona persona = opePersona.Objeto;
        ResultadoOperacionMovimientoDelUsuario opeMovimientos = new ResultadoOperacionMovimientoDelUsuario();

        // Valida desde y hasta
        if (desde >= hasta) return new ResultadoOperacionMovimientoDelUsuario(CodigosError.DatoInconsistente, "La fecha 'desde' es posterior la fecha 'hasta'");

        // Obtiene los movimientos
        foreach (Movimiento mov in persona.Movimientos.Where(m => m.Fecha >= desde && m.Fecha <= hasta).OrderBy(m => m.Fecha))
        {
            opeMovimientos.Movimientos.Add(mov);
        }
        if (!opeMovimientos.Movimientos.Any()) return new ResultadoOperacionMovimientoDelUsuario(CodigosError.NoExiste, $"No se registran movimientos en el período {desde:dd/MM/yyyy HH:mm} - {hasta:dd/MM/yyyy HH:mm}");
        return opeMovimientos;
    }
}
