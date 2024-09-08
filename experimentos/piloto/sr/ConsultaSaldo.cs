using System;
using System.Collections.Generic;
using System.Linq;
using Solucion;

namespace Operaciones;

public class ConsultaSaldo
{

    private static double ConsultaSaldoOk(string dni, List<SaldoModel> saldos)
    {
        var saldo = 0.0;
        var saldoRegistro = saldos.FirstOrDefault(x => x.Dni == dni);

        if (saldoRegistro != null)
        {
            saldo = saldoRegistro.Saldo;
        }
        return saldo;
    }

    public static RespuestaOperacion Ejecutar(string dni, string clave, Estado estado)
    {
        var respuestaOperacion = new RespuestaOperacion()
        {
            ResultadoOperacion = true,
            MensajeRespuesta = "",
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

        var saldo = ConsultaSaldoOk(dni, estado.Saldos);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "El saldo de la cuenta es de: $ " + saldo;

        Console.WriteLine(respuestaOperacion.MensajeRespuesta);

        return respuestaOperacion;
    }
}
