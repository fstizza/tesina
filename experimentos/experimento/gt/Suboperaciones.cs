using System;
using System.Collections.Generic;
using System.Linq;
using static Solucion.Estado;

namespace Solucion
{
    public static class Suboperaciones
    {
        public static (RESULTADO, int) ConsultaSaldo(Estado estado, int dni, string clave)
        {
            int saldo = 0;
            if (!estado.usuarios.Keys.Contains(dni)) return (RESULTADO.usuarioInexistente, saldo);
            if (!(estado.claves[dni] == clave)) return (RESULTADO.claveIncorrecta, saldo);

            saldo = estado.saldos[dni];

            return (RESULTADO.ok, saldo);
        }

        public static RESULTADO Extraccion(Estado estado, int dni, string clave, int monto)
        {
            if (!estado.usuarios.Keys.Contains(dni)) 
                return RESULTADO.usuarioInexistente;

            if (!(estado.claves[dni] == clave)) 
                return RESULTADO.claveIncorrecta;

            if (!(estado.movimientos[dni]
                .Where(o => FuncionesExternas.MISMO_DIA(o.Key, Globales.ahora))
                .Where(o => o.Value == OPERACION.extraccion)
                .Count() <= 2))
                return RESULTADO.noCumplePoliticaExtraccion;

            if (!(monto <= estado.sueldos[dni] / 2)) return RESULTADO.noCumplePoliticaExtraccion2;

            if (!(monto <= estado.saldo)) return RESULTADO.saldoCajeroInsuficiente;

            estado.saldo -= monto;

            estado.saldos[dni] -= monto;

            var ahora = Globales.ahora;

            if (!estado.movimientos[dni].Any(o => o.Key == ahora))
                estado.movimientos[dni].Add(ahora, OPERACION.extraccion);

            return RESULTADO.ok;
        }

        public static RESULTADO CambioClave(Estado estado, int dni, string clave, string nueva_clave)
        {
            if (!estado.usuarios.Keys.Contains(dni))
                return RESULTADO.usuarioInexistente;

            if (!(estado.claves[dni] == clave))
                return RESULTADO.claveIncorrecta;

            if (!(FuncionesExternas.LONGITUD(nueva_clave) >= Globales.LONG_MIN_CLAVE))
                return RESULTADO.noCumpleRequisitosClave1;

            if (!(FuncionesExternas.CONTIENE_LETRA_NUM(nueva_clave)))
                return RESULTADO.noCumpleRequisitosClave2;

            if (estado.movimientos[dni]
                .Any(o => FuncionesExternas.MISMO_MES(o.Key, Globales.ahora) && o.Value == OPERACION.clave))
                return RESULTADO.cambioDeClaveBloqueado;

            estado.claves[dni] = nueva_clave;

            var ahora = Globales.ahora;

            if (!estado.movimientos[dni].Any(o => o.Key == ahora))
                estado.movimientos[dni].Add(ahora, OPERACION.clave);

            return RESULTADO.ok;
        }

        public static (RESULTADO, List<(DateTime,OPERACION)>) ConsultaMovimientos(Estado estado, int dni, string clave, int dni_consulta, 
            DateTime desde, DateTime hasta)
        {
            if (!(Globales.administrador == dni))
                return (RESULTADO.usuarioNoHabilitado, null);

            if (!(estado.claves[dni] == clave))
                return (RESULTADO.claveIncorrecta, null);

            if (!estado.usuarios.Keys.Contains(dni_consulta))
                return (RESULTADO.usuarioInexistente, null);

            var movimientos = estado.movimientos[dni_consulta].Where(o => FuncionesExternas.DIF_FECHAS_DIAS(o.Key, desde) >= 0 &&
                FuncionesExternas.DIF_FECHAS_DIAS(hasta, o.Key) >= 0).Select(o => (o.Key, o.Value));

            return (RESULTADO.ok, movimientos.ToList());
        }

        public static RESULTADO AltaUsuario(Estado estado, int dni_administrador, string clave_administrador, int dni,
            string clave, string nombre, int sueldo)
        {
            if (!(Globales.administrador == dni_administrador))
                return RESULTADO.usuarioNoHabilitado;

            if (!(estado.claves[dni_administrador] == clave_administrador))
                return RESULTADO.claveIncorrecta;

            if (estado.usuarios.Keys.Contains(dni))
                return RESULTADO.usuarioYaExistente;

            if (!(estado.usuarios.Count < 5))
                return RESULTADO.limiteUsuariosAlcanzado;

            estado.movimientos.Add(dni, new Dictionary<DateTime, OPERACION>());

            estado.usuarios.Add(dni, nombre);

            estado.claves.Add(dni, clave);

            estado.saldos.Add(dni, sueldo);

            estado.sueldos.Add(dni, sueldo);

            return RESULTADO.ok;
        }

        public static RESULTADO Carga(Estado estado, int dni_administrador, string clave_administrador, int saldo)
        {
            if (!(Globales.administrador == dni_administrador))
                return RESULTADO.usuarioNoHabilitado;

            if (!(estado.claves[dni_administrador] == clave_administrador))
                return RESULTADO.claveIncorrecta;

            estado.saldo += saldo;

            return RESULTADO.ok;
        }
    }
}
