namespace Solucion;

public class Cajero : Dominio
{
    public Cajero(int id) : base(Tipos.Cajero, id)
    {
    }

    #region Propiedades
    public int IdCajero => Id;
    public decimal Saldo { get; set; }

    #endregion

    #region Operaciones
    public ResultadoOperacion IngresarDineroAlCajero(decimal importe)
    {
        // Precondiciones
        if (importe <= 0) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor a ingresar al cajero deber ser mayor que cero. Se ha recibido {importe:C2}");

        // Log
        string descripcion = $"Ingreso de dinero al cajero: Saldo anterior={Saldo:C2} Monto={importe:C2} Saldo actual={Saldo + importe:C2}";

        // Accion
        Saldo += importe;

        Movimiento mov = new Movimiento(descripcion);
        Movimientos.Add(mov);

        return new ResultadoOperacion();
    }

    public ResultadoOperacion Extraer(string apellidoYNombres, decimal importe)
    {
        // Precondiciones
        ResultadoOperacion ope = PuedeExtraer(importe);
        if (!ope.OK) return ope;

        // Log
        string descripcion = $"Extracción de {apellidoYNombres} por {importe:C2}";

        // Acción
        Saldo -= importe;

        Movimiento mov = new Movimiento(descripcion);
        Movimientos.Add(mov);

        return new ResultadoOperacion();
    }

    #endregion

    #region Precondiciones

    public ResultadoOperacion PuedeExtraer(decimal importe)
    {
        if (importe <= 0) return new ResultadoOperacion(CodigosError.ImporteIncorrecto, $"El valor a extraer del cajero deber ser mayor que cero. Se ha recibido {importe:C2}");
        if (importe > Saldo) return new ResultadoOperacion(CodigosError.SaldoInsuficiente, $"No hay saldo suficiente en el cajero para una extracción de {importe:C2}");
        return new ResultadoOperacion();
    }
    #endregion
}
