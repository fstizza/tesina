using System;

namespace Solucion;

/// <summary>
/// Actúa como fachada de las operaciones del cajero, delegando
/// en las clases especializadas cada operación y persistiendo el 
/// estado luego de cada invocación.
/// </summary>
public class Cajero
{
    private readonly IPersistenciaEstado _persistenciaEstado;
    private readonly Extraccion _extraccion;
    private readonly CambioClave _cambioClave;
    private readonly ConsultaSaldo _consultaSaldo;
    private readonly AltaUsuario _altaUsuario;
    private readonly CargaCajero _cargaCajero;
    private readonly ConsultaMovimientos _consultaMovimientos;

    public Cajero(
        IPersistenciaEstado persistenciaEstado,
        Extraccion extraccion,
        CambioClave cambioClave,
        ConsultaSaldo consultaSaldo,
        AltaUsuario altaUsuario,
        CargaCajero cargaCajero,
        ConsultaMovimientos consultaMovimientos)
    {
        _persistenciaEstado = persistenciaEstado;
        _extraccion = extraccion;
        _cambioClave = cambioClave;
        _consultaSaldo = consultaSaldo;
        _altaUsuario = altaUsuario;
        _cargaCajero = cargaCajero;
        _consultaMovimientos = consultaMovimientos;
    }

    public ResultadoExtraccion Extraccion(SolicitudExtraccion solicitud)
    {
        return EjecutarOperacion(() => _extraccion.Ejecutar(solicitud));
    }

    public ResultadoOperacion CambioClave(SolicitudCambioClave solicitud)
    {
        return EjecutarOperacion(() => _cambioClave.Ejecutar(solicitud));
    }

    public ResultadoConsultaSaldo ConsultaSaldo(SolicitudConsultaSaldo solicitud)
    {
        return EjecutarOperacion(() => _consultaSaldo.Ejecutar(solicitud));
    }

    public ResultadoAltaUsuario AltaUsuario(SolicitudAltaUsuario solicitud)
    {
        return EjecutarOperacion(() => _altaUsuario.Ejecutar(solicitud));
    }

    public ResultadoOperacion CargaCajero(SolicitudCargaCajero solicitud)
    {
        return EjecutarOperacion(() => _cargaCajero.Ejecutar(solicitud));
    }

    public ResultadoConsultaMovimientos ConsultaMovimientos(SolicitudConsultaMovimientos solicitud)
    {
        return EjecutarOperacion(() => _consultaMovimientos.Ejecutar(solicitud));
    }

    private TR EjecutarOperacion<TR>(Func<TR> invocacion)
    {
        var resultado = invocacion();

        _persistenciaEstado.Guardar();

        return resultado;
    }
}