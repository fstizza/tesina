using Solucion;

namespace Operaciones;

public class AltaUsuario
{
    // TODO: Utilizar los tipos que correspondan.
    public static ResultadoOperacion Ejecutar(int dni, string clave, int dni_usuario, string clave_usuario, string nombre, decimal saldo, decimal sueldo)
    {
        ResultadoOperacion ope;
        int cantidadMaxima = 300;

        // Obtiene el Administrador y valida sus datos
        ResultadoOperacionLeer<Administrador> opeAdm = DominioRep.LeerAdministrador<Administrador>();
        if (!opeAdm.OK) return new ResultadoOperacion(opeAdm.CodigoError, opeAdm.Mensaje);
        if (opeAdm.Objeto.DNI != dni) return new ResultadoOperacion(CodigosError.UsuarioOClaveIncorrecto, $"El usuario con DNI:{dni} no es un administrador");
        ope = opeAdm.Objeto.ValidarClave(clave);
        if (!ope.OK) return ope;

        // Valida si existe el usuario
        ope = DominioRep.Existe(Tipos.Persona, dni_usuario);
        if (ope.OK) return new ResultadoOperacion(CodigosError.UsurioExistente, $"EL usuario con DNI:{dni_usuario} ya existe.");

        // Valida los parametros de creación del usuario
        if (dni_usuario <= 0) return new ResultadoOperacion(CodigosError.DatoInconsistente, "El DNI deber ser un número entero mayor que cero");
        if (!Dominio.EsClaveSegura(clave_usuario)) return new ResultadoOperacion(CodigosError.ClaveNoSegura, "La clave ingresada no es segura. Debe poseer 8 caracteres como mínimo y ser una combionación de letras y números.");
        if (string.IsNullOrWhiteSpace(nombre)) return new ResultadoOperacion(CodigosError.DatoInconsistente, "El Apellido y Nombres del usuario no pueden estar en blanco");
        if (sueldo <= 0) return new ResultadoOperacion(CodigosError.DatoInconsistente, "El sueldo deber ser un importe mayor que cero");
        if (saldo < 0) return new ResultadoOperacion(CodigosError.DatoInconsistente, "El sueldo deber ser un importe mayor o igual a cero");

        // Verifica cuantas personas ya están asignadas al cajero.
        int cantidad = DominioRep.CantidadPersonas();
        if (cantidad >= cantidadMaxima) return new ResultadoOperacion(CodigosError.TopeCantidadUsuarios, $"Se ha alcanzado la cantidad máxima de usuarios: {cantidadMaxima} para este cajero");

        Persona persona = new Persona(dni_usuario, nombre, clave_usuario, sueldo, saldo);
        ope = DominioRep.Guardar(persona);
        return ope;
    }
}
