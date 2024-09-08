using System;
using Solucion;

namespace Operaciones;

public class AltaUsuario
{
    private static RespuestaCaminoFeliz AltaUsuarioOk(string dni_usuario, string clave_usuario, string nombre, double saldo, double sueldo, Estado estado)
    {
        estado.Usuarios.Add(new UsuarioModel()
        {
            Dni = dni_usuario,
            Nombre = nombre
        });

        estado.Claves.Add(new ClaveModel()
        {
            Dni = dni_usuario,
            Clave = clave_usuario,
        });

        estado.Saldos.Add(new SaldoModel()
        {
            Dni = dni_usuario,
            Saldo = saldo,
        });

        estado.Sueldos.Add(new SueldoModel()
        {
            Dni = dni_usuario,
            Sueldo = sueldo,
        });


        return new RespuestaCaminoFeliz()
        {
            NuevoEstado = estado,
            ValorParaMensaje = nombre,
        };
    }
    public static RespuestaOperacion Ejecutar(string dni, string clave, string dni_usuario, string clave_usuario, string nombre, double saldo, double sueldo, Estado estado)
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

        respuestaError = Errores.UsuarioYaExistente(dni_usuario, estado.Usuarios);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        respuestaError = Errores.LimiteUsuarioAlcanzado(estado.Usuarios);
        if (respuestaError.ContieneError)
        {
            respuestaOperacion.ResultadoOperacion = false;
            respuestaOperacion.MensajeRespuesta = respuestaError.MensajeError;
            Console.WriteLine(respuestaOperacion.MensajeRespuesta);
            return respuestaOperacion;
        }

        // Faltaría el checkeo de todos los requisitos de la clave en esta operación que no estan presentes en la especificación.


        var respuestaCaminoFeliz = AltaUsuarioOk(dni_usuario, clave_usuario, nombre, saldo, sueldo, estado);
        respuestaOperacion.MensajeRespuesta = Resultado.OK + "Bienvenido al barco " + respuestaCaminoFeliz.ValorParaMensaje + ".";
        respuestaOperacion.NuevoEstado = respuestaCaminoFeliz.NuevoEstado;

        // En respuestaOperacion.NuevoEstado tenemos nueestro estado actualizado. A fines prácticos mostramos solo el mensaje de respuesta de la operación.
        Console.WriteLine(respuestaOperacion.MensajeRespuesta);

        return respuestaOperacion;
    }
}
