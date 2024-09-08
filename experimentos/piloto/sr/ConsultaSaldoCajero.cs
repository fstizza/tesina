using System;
using Solucion;

namespace Operaciones;

public class ConsultaSaldoCajero
{
    public static RespuestaOperacion Ejecutar(string dni, string clave, Estado estado)
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

        respuestaError = Errores.ClaveIncorrecta(dni, clave, estado.Claves);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaOperacion.MensajeRespuesta = Resultado.OK + "El saldo del cajero es de: $ " + estado.SaldoCajero;

        Console.WriteLine(respuestaOperacion.MensajeRespuesta);

        return respuestaOperacion;
    }
}
