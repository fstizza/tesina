namespace Solucion;

public class Administrador : Dominio
{
    public Administrador(int dni, string apellidoYNombres, string clave) : base(Tipos.Administrador, dni)
    {
        ApellidoYNombres = apellidoYNombres;
        Clave = clave;
    }

    #region Propiedades

    public int DNI => Id;
    public string ApellidoYNombres { get; set; }
    public string Clave { get; set; }

    #endregion

    #region Operaciones

    public ResultadoOperacion ValidarClave(string clave)
    {
        if (clave != Clave)
        {
            return new ResultadoOperacion(CodigosError.UsuarioOClaveIncorrecto, "El DNI o la clave son incorrectos");
        }
        return new ResultadoOperacion();
    }

    #endregion
}
