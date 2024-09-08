using System;
using System.Linq;

namespace Solucion;

public class ConsultaMovimientos : Operacion
{
    private readonly IReloj _reloj;
    private readonly IUsuarios _usuarios;
    private readonly IMovimientos _movimientos;

    public ConsultaMovimientos(
        IReloj reloj,
        IUsuarios usuarios,
        IMovimientos movimientos) : base(usuarios)
    {
        _reloj = reloj;
        _usuarios = usuarios;
        _movimientos = movimientos;
    }

    public ResultadoConsultaMovimientos Ejecutar(SolicitudConsultaMovimientos solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        ResultadoConsultaMovimientos resultado;

        if (UsuarioNoAutenticado(solicitud.Dni_Administrador, solicitud.Clave_Administrador, out var usuarioAdministrador, out var codigo, out var mensaje) ||
            UsuarioNoEsAdministrador(usuarioAdministrador, out codigo, out mensaje) ||
            UsuarioConsultaNoExiste(solicitud.Dni_Consulta, out var usuarioConsulta, out codigo, out mensaje) ||
            RangoFechasEsInvalido(solicitud.Desde, solicitud.Hasta, out codigo, out mensaje))
        {
            resultado = new ResultadoConsultaMovimientos(false, null, codigo, mensaje);
        }
        else
        {
            var movimientos = _movimientos.ObtenerMovimientosPorFecha(
                usuarioConsulta, solicitud.Desde, solicitud.Hasta);

            if ((movimientos?.Count() ?? 0) == 0)
            {
                mensaje = "Sin movimientos en el período solicitado.";
            }

            resultado = new ResultadoConsultaMovimientos(true, movimientos, "CM00", mensaje);
        }

        return resultado;
    }

    private bool UsuarioConsultaNoExiste(Documento dni, out Usuario usuarioConsulta, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        usuarioConsulta = _usuarios.Obtener(dni);

        if (usuarioConsulta == null)
        {
            codigo = "CM01";
            mensaje = "No existe el usuario que desea consultar.";
        }

        return usuarioConsulta == null;
    }

    private bool RangoFechasEsInvalido(DateOnly desde, DateOnly hasta, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        bool invalido; 

        if (hasta < desde)
        {
            invalido = true;
            codigo = "CM02";
            mensaje = "La fecha HASTA no puede ser anterior a la DESDE.";
        }
        else if (hasta > DateOnly.FromDateTime(_reloj.FechaActual))
        {
            invalido = true;
            codigo = "CM03";
            mensaje = "La fecha HASTA no puede ser posterior a HOY.";
        }
        else
        {
            invalido = false;
        }
        
        return invalido;
    }
}
