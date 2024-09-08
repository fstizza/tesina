using System;

namespace Solucion;

public class CargaCajero : Operacion
{
    private readonly IGestionDinero _gestionDinero;

    public CargaCajero(
        IUsuarios usuarios,
        IGestionDinero gestionDinero) : base(usuarios)
    {
        _gestionDinero = gestionDinero;
    }

    public ResultadoOperacion Ejecutar(SolicitudCargaCajero solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        ResultadoOperacion resultado;

        if (UsuarioNoAutenticado(solicitud.Dni_Administrador, solicitud.Clave_Administrador, out var usuario, out var codigo, out var mensaje) ||
            UsuarioNoEsAdministrador(usuario, out codigo, out mensaje))
        {
            resultado = new ResultadoOperacion(false, codigo, mensaje);
        }
        else
        {
            _gestionDinero.Cargar(solicitud.Monto);

            resultado = new ResultadoOperacion(true, "RC00", "Recarga exitosa del cajero.");
        }

        return resultado;
    }
}
