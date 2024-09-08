using Microsoft.Extensions.DependencyInjection;
using System;

namespace Solucion;

/// <summary>
/// Factoria para el cajero, usando un inyector de dependencias.
/// </summary>
public class CajeroFactoria
{
    private readonly static IServiceProvider _contenedor;

    static CajeroFactoria()
    {
        _contenedor = ConfigurarInyector();
    }

    public static Cajero InstanciarCajero()
    {
        return ActivatorUtilities.CreateInstance<Cajero>(_contenedor);
    }

    private static IServiceProvider ConfigurarInyector()
    {
        var servicios = new ServiceCollection();

        servicios.AddSingleton<IReloj, Reloj>();

        servicios.AddSingleton<PoliticaExtracciones>();
        servicios.AddSingleton<PoliticaSeguridad>();

        servicios.AddSingleton<Extraccion>();
        servicios.AddSingleton<CambioClave>();
        servicios.AddSingleton<ConsultaSaldo>();
        servicios.AddSingleton<AltaUsuario>();
        servicios.AddSingleton<CargaCajero>();
        servicios.AddSingleton<ConsultaMovimientos>();

        var estado = Estado.Cargar();
        var persistenciaEstado = new PersistenciaEstado(estado);
        servicios.AddSingleton<IPersistenciaEstado>(persistenciaEstado);

        servicios.AddSingleton<IGestionDinero, GestionDinero>();
        servicios.AddSingleton<IEstadoDinero>(persistenciaEstado);

        servicios.AddSingleton<IUsuarios, Usuarios>();
        servicios.AddSingleton<IEstadoUsuarios>(persistenciaEstado);

        servicios.AddSingleton<IMovimientos, Movimientos>();
        servicios.AddSingleton<IEstadoMovimientos>(persistenciaEstado);

        servicios.AddSingleton<IHistorialCambiosClave, HistorialCambiosClave>();
        servicios.AddSingleton<IEstadoHistorialCambiosClave>(persistenciaEstado);
        
        return servicios.BuildServiceProvider();
    }
}
