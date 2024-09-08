namespace Solucion;

public class Soporte
{
    public static ResultadoOperacion ValidarAdministrador(int dni, string clave)
    {
        ResultadoOperacion ope;

        ResultadoOperacionLeer<Administrador> opeAdm = DominioRep.LeerAdministrador<Administrador>();
        if (!opeAdm.OK) return new ResultadoOperacion(opeAdm.CodigoError, opeAdm.Mensaje);
        if (opeAdm.Objeto.DNI != dni) return new ResultadoOperacion(CodigosError.UsuarioOClaveIncorrecto, $"El usuario con DNI:{dni} no es un administrador");
        ope = opeAdm.Objeto.ValidarClave(clave);
        return ope;
    }

    public static ResultadoOperacionLeer<T> ValidarPersona<T>(int dni, string clave) where T:Persona
    {
        ResultadoOperacion ope;

        ResultadoOperacionLeer<T> opePersona = DominioRep.Leer<T>(Tipos.Persona,dni);
        if (!opePersona.OK) return new ResultadoOperacionLeer<T>(opePersona.CodigoError, opePersona.Mensaje);
        ope = opePersona.Objeto.ValidarClave(clave);
        if (!ope.OK) return new ResultadoOperacionLeer<T>(ope.CodigoError, ope.Mensaje);
        return opePersona;
    }

}
