namespace Solucion;

public class Inicializar
{
    public static ResultadoOperacion Ejecutar(int dni, string apellidoYNombres, string clave)
    {
        // Verifica si existe el administrador
        ResultadoOperacion opExisteAdm = DominioRep.ExisteAdministrador();
        if (!opExisteAdm.OK)
        {
            Administrador adm = new Administrador(dni, apellidoYNombres, clave);
            opExisteAdm = DominioRep.Guardar(adm);
            if (!opExisteAdm.OK) return opExisteAdm;
        }
        else
        {
            ResultadoOperacionLeer<Administrador> opLeerAdm = DominioRep.LeerAdministrador<Administrador>();
            if (opLeerAdm.OK && opLeerAdm.Objeto.Id != dni)
            {
                return new ResultadoOperacion(CodigosError.AdministradorIncorrecto, "El administrador ya existe y no corresponde al DNI ingresado, debe eliminar el existente y volver a inicializar.");
            }
            if (opLeerAdm.OK && !opLeerAdm.Objeto.ValidarClave(clave).OK)
            {
                return new ResultadoOperacion(CodigosError.AdministradorIncorrecto, "El administrador ya existe y no corresponde su clave, debe eliminar el existente y volver a inicializar.");
            }
        }


        // Verifica la existencia del cajero con Id = 1
        ResultadoOperacion opExisteCajero = DominioRep.Existe(Tipos.Cajero, 1);
        if (!opExisteCajero.OK)
        {
            Cajero cajero = new Cajero(1);
            opExisteCajero = DominioRep.Guardar(cajero);
            if (!opExisteCajero.OK)
            {
                return opExisteCajero;
            }
        }
        return new ResultadoOperacion();
    }
}
