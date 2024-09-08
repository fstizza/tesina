using Solucion;
using System;
using System.Linq;

namespace Operaciones;

public class ConsultaMovimientos
{
    private static RespuestaCaminoFeliz ConsultaMovimientoOk(string dni_consulta, DateTime desde, DateTime hasta, Estado estado)
    {
        var listado = "";

        var movimientos = estado.Movimientos
            .Where(x => x.Dni == dni_consulta && Utiles.DifFechaDias(x.Movimiento.Fecha, desde) >= 0 && Utiles.DifFechaDias(hasta, x.Movimiento.Fecha ) >= 0)
            .ToList();

        foreach (var movimiento in movimientos)
        {
            listado = listado + movimiento.Movimiento.Fecha + " " +
                      movimiento.Movimiento.Operacion + ". ";
        }

        return new RespuestaCaminoFeliz()
        {
            NuevoEstado = estado,
            ValorParaMensaje = listado,
        };
    }

    public static RespuestaOperacion Ejecutar(string dni, string clave, string dni_consulta, DateTime desde, DateTime hasta, Estado estado)
    {
        var respuestaOperacion = new RespuestaOperacion()
        {
            ResultadoOperacion = true,
            MensajeRespuesta = "",
        };

        var respuestaError = Errores.UsuarioNoHabilitado(dni);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.UsuarioInexistente(dni, estado.Usuarios);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.ClaveIncorrecta(dni, clave, estado.Claves);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        var respuestaCaminoFeliz = ConsultaMovimientoOk(dni_consulta, desde, hasta, estado);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "Listado de movimientos : $ " + respuestaCaminoFeliz.ValorParaMensaje;
        respuestaOperacion.NuevoEstado = respuestaCaminoFeliz.NuevoEstado;

        // En respuestaOperacion.NuevoEstado tenemos nueestro estado actualizado. A fines prácticos mostramos solo el mensaje de respuesta de la operación.
        Console.WriteLine(respuestaOperacion.MensajeRespuesta);

        return respuestaOperacion;
    }
}
