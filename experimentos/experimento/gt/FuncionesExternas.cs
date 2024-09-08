using System;
using System.Linq;

namespace Solucion
{
    public static class FuncionesExternas
    {
        public static bool MISMO_MES(DateTime fechaHora1, DateTime fechaHora2)
        {
            return fechaHora1.Year == fechaHora1.Year && fechaHora1.Month == fechaHora2.Month;
        }
        public static bool MISMO_DIA(DateTime fechaHora1, DateTime fechaHora2)
        {
            return fechaHora1.Year == fechaHora1.Year && fechaHora1.Month == fechaHora2.Month && fechaHora1.Day == fechaHora2.Day;
        }

        public static int LONGITUD(string clave)
        {
            return clave.Length;
        }

        public static bool CONTIENE_LETRA_NUM(string cadena)
        {
            return cadena.ToCharArray().All(c => Char.IsLetterOrDigit(c));
        }

        public static int DIF_FECHAS_DIAS(DateTime fechaHora1, DateTime fechaHora2)
        {
            return (int)Math.Truncate((fechaHora1 - fechaHora2).TotalDays);
        }
    }
}
