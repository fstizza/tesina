using System;

namespace Solucion;

public class ConsultaSaldo : Operacion
{
    private readonly IMovimientos _movimientos;

    public ConsultaSaldo(
        IUsuarios usuarios,
        IMovimientos movimientos) : base(usuarios)
    {
        _movimientos = movimientos;
    }

    public ResultadoConsultaSaldo Ejecutar(SolicitudConsultaSaldo solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        ResultadoConsultaSaldo resultado;

        if (UsuarioNoAutenticado(solicitud.Dni, solicitud.Clave, out var usuario, out var codigo, out var mensaje))
        {
            resultado = new ResultadoConsultaSaldo(false, null, codigo, mensaje);
        }
        else
        {
            resultado = new ResultadoConsultaSaldo(
                true, _movimientos.ObtenerSaldoActualCuenta(usuario), "CS00", null);
        }

        return resultado;
    }
}
