using Solucion;
using System;

namespace Operaciones;

public class CambioClave
{
    public static ResultadoOperacion Ejecutar(int dni, string clave, string nueva_clave)
    {
        ResultadoOperacion ope;

        // Obtiene la persona
        ResultadoOperacionLeer<Persona> opeLeerPersona = DominioRep.Leer<Persona>(Tipos.Persona, dni);
        if (!opeLeerPersona.OK) return new ResultadoOperacion(opeLeerPersona.CodigoError, opeLeerPersona.Mensaje);
        
        Persona persona = opeLeerPersona.Objeto;
        ope = persona.ValidarClave(clave);
        if (!ope.OK) return ope;

        if (clave == nueva_clave) return new ResultadoOperacion(CodigosError.DatoInconsistente, "La nueva clave debe ser distinta a la actual");
        if (!Dominio.EsClaveSegura(nueva_clave)) return new ResultadoOperacion(CodigosError.ClaveNoSegura, "La clave ingresada no es segura. Debe poseer 8 caracteres como mínimo y ser una combionación de letras y números");
        if (persona.UltimoCambioDeClave != null && persona.UltimoCambioDeClave?.ToString("yyyyMM") == DateTime.Now.ToString("yyyyMM"))
        {
            return new ResultadoOperacion(CodigosError.TopeCambioClave, $"Solo se permite el cambio de calve una vez por mes. Último cambio:{persona.UltimoCambioDeClave:yyyy/MM/dd HH:mm:ss}");
        }
        persona.Clave = nueva_clave;
        persona.UltimoCambioDeClave = DateTime.Now;

        ope = DominioRep.Guardar(persona);
        return ope;
    }
}
