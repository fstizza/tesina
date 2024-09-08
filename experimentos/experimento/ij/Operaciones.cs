using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Solucion
{




    public static class Operaciones
    {
        static Estado _estado;

        /// <summary>
        /// Da de alta un nuevo usuario en el cajero
        /// </summary>
        /// <param name="DNI_Admin"></param>
        /// <param name="CLAVE_Admin"></param>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="NOMBRE"></param>
        /// <param name="SUELDO"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion AltaUsuario(int? DNI_Admin, string CLAVE_Admin, int? DNI, string CLAVE, string NOMBRE, decimal? SUELDO)
        {

            _estado = Estado.Cargar();

            try
            {

                if (!ValidarUsuario(DNI_Admin)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioInexistente); }

                if (!ValidarClave(DNI_Admin, CLAVE_Admin))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Alta, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                if (ValidarUsuario(DNI))
                {
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioYaExistente);
                }

                if (!ValidarLimiteUsuarios())
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Alta, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.LimiteUsuariosAlcanzado });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.LimiteUsuariosAlcanzado);
                }

                Usuario usuario = new()
                {
                    DNI = DNI.Value,
                    Clave = CLAVE,
                    Nombre = NOMBRE,
                    Saldo = SUELDO ?? 0,
                    Sueldo = SUELDO ?? 0,
                    Operaciones = new List<Operacion>(),
                };

                usuario.Operaciones.Add(new Operacion()
                {
                    TipoOperacion = Operacion.TiposOperacion.Alta,
                    FechaOperacion = DateTime.Now,
                    Monto = SUELDO,
                    Resultado = ResultadoOperacion.Resultados.OK,
                    Saldo = 0,
                });

                _estado.Usuarios.Add(usuario);

                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }

        }

        /// <summary>
        /// Retorna el saldo de la cuenta del usuario autenticado
        /// </summary>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="MONTO"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion ConsultaSaldo(int? DNI, string CLAVE, ref decimal? MONTO)
        {

            _estado = Estado.Cargar();

            try
            {

                if (!ValidarUsuario(DNI)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioYaExistente); }

                if (!ValidarClave(DNI, CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Saldo, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                MONTO = _estado.UsuarioActual.Saldo;


                _estado.UsuarioActual.Operaciones.Add(new Operacion()
                {
                    TipoOperacion = Operacion.TiposOperacion.Saldo,
                    FechaOperacion = DateTime.Now,
                    Monto = null,
                    Resultado = ResultadoOperacion.Resultados.OK,
                    Saldo = _estado.UsuarioActual.Saldo,
                });


                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }

        }

        /// <summary>
        /// Extrae el monto especificado de la cuenta del usuario autenticado
        /// </summary>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="MONTO"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion Extraccion(int? DNI, string CLAVE, decimal? MONTO)
        {

            _estado = Estado.Cargar();

            try
            {

                if (!ValidarUsuario(DNI)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioInexistente); }

                if (!ValidarClave(DNI, CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Extraccion, FechaOperacion = DateTime.Now, Monto = MONTO, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                if (!ValidarPoliticaExtraccion(DNI))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Extraccion, FechaOperacion = DateTime.Now, Monto = MONTO, Resultado = ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion);
                }

                if (!ValidarPoliticaExtraccion(DNI, MONTO))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Extraccion, FechaOperacion = DateTime.Now, Monto = MONTO, Resultado = ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion2 });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.NoCumplePoliticaExtraccion2);
                }

                if (!ValidarSaldo(DNI, MONTO))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Extraccion, FechaOperacion = DateTime.Now, Monto = MONTO, Resultado = ResultadoOperacion.Resultados.SaldoInsuficiente });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.SaldoInsuficiente);
                }

                if (!ValidarSaldoCajero(DNI, MONTO))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Extraccion, FechaOperacion = DateTime.Now, Monto = MONTO, Resultado = ResultadoOperacion.Resultados.SaldoCajeroInsuficiente });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.SaldoCajeroInsuficiente);
                }

                _estado.UsuarioActual.Saldo = _estado.UsuarioActual.Saldo - MONTO.Value;

                //OK
                _estado.UsuarioActual.Operaciones.Add(new Operacion()
                {
                    TipoOperacion = Operacion.TiposOperacion.Extraccion,
                    FechaOperacion = DateTime.Now,
                    Monto = MONTO,
                    Resultado = ResultadoOperacion.Resultados.OK,
                    Saldo = _estado.UsuarioActual.Saldo,
                });


                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);


            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }

        }

        /// <summary>
        /// Asignar la nueva clave especificada al usuario autenticado
        /// </summary>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="NUEVA_CLAVE"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion CambioClave(int? DNI, string CLAVE, string NUEVA_CLAVE)
        {

            try
            {

                _estado = Estado.Cargar();

                if (!ValidarUsuario(DNI)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioInexistente); }

                if (!ValidarClave(DNI, CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.CambioClave, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                if (!ValidarRequisitorClave())
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.CambioClave, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.NoCumpleRequisitosClave1 });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.NoCumpleRequisitosClave1);
                }

                if (!ValidarRequisitorClave2(NUEVA_CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.CambioClave, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.NoCumpleRequisitosClave2 });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.NoCumpleRequisitosClave2);
                }

                //OK
                _estado.UsuarioActual.Operaciones.Add(new Operacion()
                {
                    TipoOperacion = Operacion.TiposOperacion.CambioClave,
                    FechaOperacion = DateTime.Now,
                    Monto = null,
                    Resultado = ResultadoOperacion.Resultados.OK,
                    Saldo = _estado.UsuarioActual.Saldo,
                });

                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }
        }

        /// <summary>
        /// Acredita el monto especificado al cajero.
        /// </summary>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="MONTO"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion Carga(int? DNI, string CLAVE, decimal? MONTO)
        {
            _estado = Estado.Cargar();

            try
            {
                if (!ValidarUsuario(DNI)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioYaExistente); }

                if (!ValidarClave(DNI, CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.Carga, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                _estado.Saldo += MONTO.Value;

                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }
        }

        /// <summary>
        /// Retorna los movimientos realizados por el usuario en el rango de fechas especificado
        /// </summary>
        /// <param name="DNI"></param>
        /// <param name="CLAVE"></param>
        /// <param name="DNI_Consulta"></param>
        /// <param name="FECHAHORA_Desde"></param>
        /// <param name="FECHAHORA_Hasta"></param>
        /// <param name="MOVIMIENTOS"></param>
        /// <returns></returns>
        /// <exception cref="NotImplementedException"></exception>
        public static ResultadoOperacion ConsultaMovimientos(int? DNI, string CLAVE, int? DNI_Consulta, DateTime? FECHAHORA_Desde, DateTime? FECHAHORA_Hasta, ref List<Operacion> MOVIMIENTOS)
        {
            _estado = Estado.Cargar();

            try
            {
                if (!ValidarUsuario(DNI)) { return new ResultadoOperacion(ResultadoOperacion.Resultados.UsuarioYaExistente); }

                if (!ValidarClave(DNI, CLAVE))
                {
                    _estado.UsuarioActual.Operaciones.Add(new Operacion() { TipoOperacion = Operacion.TiposOperacion.ConsultaMovimientos, FechaOperacion = DateTime.Now, Monto = null, Resultado = ResultadoOperacion.Resultados.ClaveIncorrecta });
                    return new ResultadoOperacion(ResultadoOperacion.Resultados.ClaveIncorrecta);
                }

                var usuarioConsulta = _estado.Usuarios.FirstOrDefault(u => u.DNI == DNI_Consulta);

                MOVIMIENTOS = usuarioConsulta.Operaciones.Where(o => o.FechaOperacion >= FECHAHORA_Desde &&
                                                                     o.FechaOperacion <= FECHAHORA_Hasta &&
                                                                     (o.TipoOperacion == Operacion.TiposOperacion.Alta ||
                                                                      o.TipoOperacion == Operacion.TiposOperacion.Carga ||
                                                                      o.TipoOperacion == Operacion.TiposOperacion.Extraccion))
                                                               .OrderByDescending(o => o.FechaOperacion).ToList();

                _estado.UsuarioActual.Operaciones.Add(new Operacion()
                {
                    TipoOperacion = Operacion.TiposOperacion.ConsultaMovimientos,
                    FechaOperacion = DateTime.Now,
                    Monto = null,
                    Resultado = ResultadoOperacion.Resultados.OK
                });

                _estado.Guardar();

                return new ResultadoOperacion(ResultadoOperacion.Resultados.OK);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return new ResultadoOperacion(ResultadoOperacion.Resultados.ErrorNoControlado);
            }

        }


        private static bool ValidarUsuario(int? dni)
        {
            if (dni == null) { return false; }

            _estado.Seleccionar(dni.Value);

            if (_estado.UsuarioActual == null) { return false; }

            return true;
        }

        private static bool ValidarClave(int? dni, string clave)
        {
            if (!ValidarUsuario(dni)) { return false; }

            if (_estado.UsuarioActual.Clave != clave) { return false; }

            return true;
        }

        private static bool ValidarPoliticaExtraccion(int? dNI)
        {
            return _estado.UsuarioActual.Operaciones.Count(
                o => o.TipoOperacion == Operacion.TiposOperacion.Extraccion &&
                     o.Resultado == ResultadoOperacion.Resultados.OK &&
                     o.FechaOperacion.Date == DateTime.Now.Date
            ) < 3;
        }

        private static bool ValidarPoliticaExtraccion(int? dNI, decimal? mONTO)
        {
            return mONTO <= (int)(_estado.UsuarioActual.Sueldo / 2);
        }

        private static bool ValidarSaldo(int? dNI, decimal? mONTO)
        {
            return mONTO <= _estado.UsuarioActual.Saldo;
        }

        private static bool ValidarSaldoCajero(int? dNI, decimal? mONTO)
        {
            return mONTO <= _estado.Saldo;
        }

        private static bool ValidarLimiteUsuarios()
        {
            return _estado.Usuarios.Count < 5;
        }

        private static bool ValidarRequisitorClave2(string cLAVE)
        {
            return cLAVE.Any(char.IsDigit) && cLAVE.Any(char.IsLetter) && cLAVE.Length >= 8;
        }

        private static bool ValidarRequisitorClave()
        {
            return _estado.UsuarioActual.Operaciones.Where(
                o =>
                {
                    var ahora = DateTime.Now.Date;
                    var fecha = o.FechaOperacion.Date;

                    return o.TipoOperacion == Operacion.TiposOperacion.CambioClave &&
                     o.Resultado == ResultadoOperacion.Resultados.OK &&
                     ahora.Year == fecha.Year &&
                     ahora.Day == fecha.Day;
                }
            ).Count() == 0;
        }
    }



    public class ResultadoOperacion
    {

        public enum Resultados
        {
            OK = 0,
            UsuarioInexistente,
            ClaveIncorrecta,
            NoCumplePoliticaExtraccion,
            NoCumplePoliticaExtraccion2,
            SaldoInsuficiente,
            SaldoCajeroInsuficiente,
            ErrorNoControlado,
            UsuarioYaExistente,
            LimiteUsuariosAlcanzado,
            NoCumpleRequisitosClave1,
            NoCumpleRequisitosClave2,
        }

        public ResultadoOperacion(Resultados resultado)
        {
            Resultado = resultado;
        }

        public Resultados Resultado { get; }

    }
}
