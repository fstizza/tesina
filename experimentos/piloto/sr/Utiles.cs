using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace Solucion
{
    public class Utiles
    {

        public static bool MismoMes(DateTime fecha, int mes)
        {
            return fecha.Month == mes;
        }

        public static bool MismoDia(DateTime fecha, int dia)
        {
            return fecha.Day == dia;
        }

        public static int DifFechaDias(DateTime fecha1, DateTime fecha2)
        {
            TimeSpan diferencia = fecha1 - fecha2;
            return (int)diferencia.TotalDays;
        }

        public static bool ContieneLetraNum(string texto)
        {
            Regex regex = new(@"^(?=.*[a-zA-Z])(?=.*\d).+$");
            return regex.IsMatch(texto);
        }

    }
    public class RespuestaError
    {
        public bool ContieneError { get; set; }
        public string MensajeError { get; set; }
    }

    public class RespuestaOperacion
    {
        public bool ResultadoOperacion { get; set; }
        public string MensajeRespuesta { get; set; }
        public Estado NuevoEstado { get; set; }
    }

    public class RespuestaCaminoFeliz
    {
        public string ValorParaMensaje { get; set; }
        public Estado NuevoEstado { get; set; }
    }
}