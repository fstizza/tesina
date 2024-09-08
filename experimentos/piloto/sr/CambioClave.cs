using Solucion;
using System;

namespace Operaciones;

public class CambioClave
{
    private static RespuestaCaminoFeliz CambioClaveOk(string dni, string nueva_clave, Estado estado)
    {
        foreach (var clave in estado.Claves)
        {
            if (clave.Dni == dni)
            {
                clave.Clave = nueva_clave;
            }
        }

        estado.Movimientos.Add(new MovimientoModel()
        {
            Dni = dni,
            Movimiento = new Movimiento()
            {
                Fecha = Constantes.AHORA,
                Operacion = OperacionTipo.CLAVE,
            }
        });


        return new RespuestaCaminoFeliz()
        {
            NuevoEstado = estado,
            ValorParaMensaje = nueva_clave,
        };
    }
    public static RespuestaOperacion Ejecutar(string dni, string clave, string nueva_clave, Estado estado)
    {
        var respuestaOperacion = new RespuestaOperacion()
        {
            ResultadoOperacion = true,
            MensajeRespuesta = "",
            NuevoEstado = estado,
        };

        var respuestaError = Errores.UsuarioInexistente(dni, estado.Usuarios);
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

        respuestaError = Errores.CambioDeClaveBloqueado(dni, estado.Movimientos);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.NoCumpleRequisitosClave1(nueva_clave);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.NoCumpleRequisitosClave2(nueva_clave);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        var respuestaCaminoFeliz = CambioClaveOk(dni, nueva_clave, estado);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "Nueva clave: " + respuestaCaminoFeliz.ValorParaMensaje;
        respuestaOperacion.NuevoEstado = respuestaCaminoFeliz.NuevoEstado;

        // En respuestaOperacion.NuevoEstado tenemos nueestro estado actualizado. A fines prácticos mostramos solo el mensaje de respuesta de la operación.
        Console.WriteLine(respuestaOperacion.MensajeRespuesta);
        return respuestaOperacion;
    }
}
