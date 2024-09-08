using System.Collections.Generic;

namespace Solucion;

public class ResultadoOperacion
{
    //private Dictionary<CodigosError, string> Errores = new Dictionary<CodigosError, string>()
    //{
    //    {CodigosError.OK, "" },
    //    {CodigosError.SaldoInsuficiente, "Saldo insuficiente" }
    //};

    public ResultadoOperacion() { }
    public ResultadoOperacion(CodigosError codigoError)
    {
        CodigoError = codigoError;
    }
    public ResultadoOperacion(CodigosError codigoError, string mensaje)
    {
        CodigoError = codigoError;
        Mensaje = mensaje;
    }

    public bool OK => CodigoError == 0;
    public CodigosError CodigoError { get; }
    public string Mensaje { get; }
}

public class ResultadoOperacionLeer<T> : ResultadoOperacion
{
    public ResultadoOperacionLeer() : base() { }
    public ResultadoOperacionLeer(T o) : base() { Objeto = o; }
    public ResultadoOperacionLeer(CodigosError codigoError) : base(codigoError) { }
    public ResultadoOperacionLeer(CodigosError codigoError, string mensaje) : base(codigoError, mensaje) { }
    public ResultadoOperacionLeer(ResultadoOperacion ope) : base(ope.CodigoError, ope.Mensaje) { }
    public T Objeto { get; set; }
}
public class ResultadoOperacionSaldoEnCajero : ResultadoOperacion
{
    public ResultadoOperacionSaldoEnCajero() : base() { }
    public ResultadoOperacionSaldoEnCajero(decimal saldo) : base() { Saldo = saldo; }
    public ResultadoOperacionSaldoEnCajero(CodigosError codigoError) : base(codigoError) { }
    public ResultadoOperacionSaldoEnCajero(CodigosError codigoError, string mensaje) : base(codigoError, mensaje) { }
    public ResultadoOperacionSaldoEnCajero(ResultadoOperacion ope) : base(ope.CodigoError, ope.Mensaje) { }
    public decimal Saldo { get; set; }
}

public class ResultadoOperacionMovimientoDelUsuario : ResultadoOperacion
{
    public ResultadoOperacionMovimientoDelUsuario() : base() { }
    public ResultadoOperacionMovimientoDelUsuario(CodigosError codigoError) : base(codigoError) { }
    public ResultadoOperacionMovimientoDelUsuario(CodigosError codigoError, string mensaje) : base(codigoError, mensaje) { }
    public ResultadoOperacionMovimientoDelUsuario(ResultadoOperacion ope) : base(ope.CodigoError, ope.Mensaje) { }
    public List<Movimiento> Movimientos { get; set; } = new List<Movimiento>();
}

