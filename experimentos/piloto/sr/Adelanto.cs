using Solucion;
using System;

namespace Operaciones;

public class Adelanto
{
    private static RespuestaCaminoFeliz AdelantoOk(string dni, double montoRequerido, Estado estado)
    {
        var nuevoSaldo = 0.0;
        foreach (var saldo in estado.Saldos)
        {
            if (saldo.Dni == dni)
            {
                nuevoSaldo = saldo.Saldo + montoRequerido;
                saldo.Saldo = nuevoSaldo;
            }
        }

        estado.Movimientos.Add(new MovimientoModel()
        {
            Dni = dni,
            Movimiento = new Movimiento()
            {
                Fecha = Constantes.AHORA,
                Operacion = OperacionTipo.ADELANTO,
            }
        });

        return new RespuestaCaminoFeliz()
        {
            NuevoEstado = estado,
            ValorParaMensaje = nuevoSaldo.ToString(),
        };
    }

    public RespuestaOperacion Ejecutar(string dni, string clave, double montoRequerido, Estado estado)
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

        respuestaError = Errores.NoCumplePoliticaAdelanto(dni, estado.Movimientos);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.NoCumplePoliticaExtraccionAdelanto(dni, montoRequerido, estado.Sueldos);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        var respuestaCaminoFeliz = AdelantoOk(dni, montoRequerido, estado);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "El nuevo saldo de la cuenta es de: $ " + respuestaCaminoFeliz.ValorParaMensaje;
        respuestaOperacion.NuevoEstado = respuestaCaminoFeliz.NuevoEstado;

        // En respuestaOperacion.NuevoEstado tenemos nueestro estado actualizado. A fines prácticos mostramos solo el mensaje de respuesta de la operación.
        Console.WriteLine(respuestaOperacion.MensajeRespuesta);
        return respuestaOperacion;
    }
}
