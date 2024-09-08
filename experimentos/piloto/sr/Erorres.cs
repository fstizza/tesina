using System;
using System.Collections.Generic;
using System.Linq;

namespace Solucion
{
    public class Errores
    {

        public static RespuestaError UsuarioInexistente(string dni, List<UsuarioModel> usuarios)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = usuarios.FirstOrDefault(x => x.Dni == dni) == null,
                MensajeError = Resultado.USUARIO_INEXISTENTE,
            };
            return respuesta;
        }

        public static RespuestaError UsuarioYaExistente(string dni, List<UsuarioModel> usuarios)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = usuarios.FirstOrDefault(x => x.Dni == dni) != null,
                MensajeError = Resultado.USUARIO_YA_EXISTENTE,
            };
            return respuesta;
        }

        public static RespuestaError ClaveIncorrecta(string dni, string clave, List<ClaveModel> claves)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = claves.FirstOrDefault(x => x.Dni == dni && x.Clave == clave) == null,
                MensajeError = Resultado.CLAVE_INCORRECTA,
            };
            return respuesta;
        }

        public static RespuestaError SaldoCajeroInsuficiente(double saldoCajero, double montoRequerido)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = montoRequerido > saldoCajero,
                MensajeError = Resultado.SALDO_CAJERO_INSUFICIENTE,
            };
            return respuesta;
        }

        public static RespuestaError SaldoInsuficiente(string dni, double montoRequerido, List<SaldoModel> saldos)
        {

            var saldo = saldos.FirstOrDefault(x => x.Dni == dni);

            var respuesta = new RespuestaError()
            {
                ContieneError = montoRequerido > saldo.Saldo,
                MensajeError = Resultado.SALDO_INSUFICIENTE,
            };
            return respuesta;
        }

        public static RespuestaError NoCumplePoliticaExtraccion(string dni, List<MovimientoModel> movimientos)
        {
            var extracciones = movimientos.Where(x => x.Dni == dni && 
                            Utiles.MismoDia(DateTime.Now, Constantes.AHORA.Day) &&
                            x.Movimiento.Operacion == OperacionTipo.EXTRACCION).ToList();

            var respuesta = new RespuestaError()
            {
                ContieneError = extracciones.Count > 2,
                MensajeError = Resultado.NO_CUMPLE_POLITICA_EXTRACCION,
            };
            return respuesta;
        }

        public static RespuestaError NoCumplePoliticaExtraccionAdelanto(string dni, double montoRequerido, List<SueldoModel> sueldos)
        {
            var sueldo = sueldos.FirstOrDefault(x => x.Dni == dni);
            var mitadSueldo = sueldo.Sueldo / 2;

            var respuesta = new RespuestaError()
            {
                ContieneError = montoRequerido > mitadSueldo,
                MensajeError = Resultado.NO_CUMPLE_POLITICA_EXTRACCION_ADELANTO,
            };
            return respuesta;
        }

        public static RespuestaError NoCumplePoliticaAdelanto(string dni, List<MovimientoModel> movimientos)
        {
            var adelantos = movimientos.Where(x => x.Dni == dni && 
                            Utiles.MismoMes(DateTime.Now, Constantes.AHORA.Month) &&
                            x.Movimiento.Operacion == OperacionTipo.ADELANTO).ToList();

            var respuesta = new RespuestaError()
            {
                ContieneError = adelantos.Any(),
                MensajeError = Resultado.NO_CUMPLE_POLITICA_ADELANTO,
            };
            return respuesta;
        }

        public static RespuestaError LimiteUsuarioAlcanzado(List<UsuarioModel> usuarios)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = usuarios.Count >= Constantes.CANT_MAX_USUARIOS,
                MensajeError = Resultado.LIMITE_USUARIOS_ALCANZADO,
            };
            return respuesta;
        }

        public static RespuestaError CambioDeClaveBloqueado(string dni, List<MovimientoModel> movimientos)
        {
            var operacionesClave = movimientos.Where(x => x.Dni == dni &&
                                                   Utiles.MismoMes(DateTime.Now, Constantes.AHORA.Month) &&
                                                   x.Movimiento.Operacion == OperacionTipo.CLAVE).ToList();

            var respuesta = new RespuestaError()
            {
                ContieneError = operacionesClave.Any(),
                MensajeError = Resultado.CAMBIO_DE_CLAVE_BLOQUEADO,
            };
            return respuesta;
        }

        public static RespuestaError UsuarioNoHabilitado(string dni)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = dni != Constantes.DNI_ADMINISTRADOR,
                MensajeError = Resultado.USUARIO_NO_HABILITADO,
            };
            return respuesta;
        }

        public static RespuestaError NoCumpleRequisitosClave1(string clave)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError =  clave.Length < Constantes.LONG_MIN_CLAVE,
                MensajeError = Resultado.NO_CUMPLE_REQUISITOS_CLAVE_1,
            };
            return respuesta;
        }

        public static RespuestaError NoCumpleRequisitosClave2(string clave)
        {
            var respuesta = new RespuestaError()
            {
                ContieneError = !Utiles.ContieneLetraNum(clave),
                MensajeError = Resultado.NO_CUMPLE_REQUISITOS_CLAVE_2,
            };
            return respuesta;
        }

    }
}

