using System.Collections.Generic;

namespace Solucion;

public abstract class Dominio
{
    #region Constructores
    public Dominio(Tipos tipo,
        int id)
    {
        Tipo = tipo;
        Id = id;
    }
    #endregion

    #region Propiedades

    public Tipos Tipo { get; }
    public int Id { get; }
    public List<Movimiento> Movimientos { get; set; } = new List<Movimiento>();

    #endregion

    #region Validaciones

    public static bool EsClaveSegura(string clave)
    {
        // ToDo: Aplicar la política de claves seguras
        return true;
    }
    #endregion

}
