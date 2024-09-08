using System.Collections.Generic;

namespace Solucion;

public class PersistenciaEstado 
    : IEstadoUsuarios, IEstadoMovimientos, IEstadoDinero, IEstadoHistorialCambiosClave, IPersistenciaEstado
{
    private readonly Estado _estado;

    public PersistenciaEstado(Estado estado)
    {
        _estado = estado;
    }

    public IDictionary<int, Usuario> Usuarios => _estado.Usuarios;

    public IList<Movimiento> Movimientos => _estado.Movimientos;

    public decimal DineroDisponible
    {
        get => _estado.DineroDisponible;
        set => _estado.DineroDisponible = value;
    }

    public IDictionary<int, IList<RegistroCambioClave>> CambiosClave => _estado.CambiosClave;

    public void Guardar()
    {
        _estado.Guardar();
    }
}
