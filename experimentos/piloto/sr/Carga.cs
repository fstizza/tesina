using Solucion;
using System;

namespace Operaciones;

public class Carga
{
    private static RespuestaCaminoFeliz CargaOk(double saldo, Estado estado)
    {
        estado.SaldoCajero -= saldo;

        return new RespuestaCaminoFeliz()
        {
            NuevoEstado = estado,
            ValorParaMensaje = estado.SaldoCajero.ToString(),
        };
    }
    public static object Ejecutar(string dni, string clave, double saldo, Estado estado)
    {
        var respuestaOperacion = new RespuestaOperacion()
        {
            ResultadoOperacion = true,
            MensajeRespuesta = "",
            NuevoEstado = estado,
        };

        var respuestaError = Errores.UsuarioNoHabilitado(dni);
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

        var respuestaCaminoFeliz = CargaOk(saldo, estado);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "Nuevo saldo: " + respuestaCaminoFeliz.ValorParaMensaje + ".";
        respuestaOperacion.NuevoEstado = respuestaCaminoFeliz.NuevoEstado;

        // En respuestaOperacion.NuevoEstado tenemos nueestro estado actualizado. A fines prácticos mostramos solo el mensaje de respuesta de la operación.
        Console.WriteLine(respuestaOperacion.MensajeRespuesta);

        return respuestaOperacion;
    }
}