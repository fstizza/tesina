using System.Collections.Generic;

namespace Solucion
{
    public class UsuarioModel
    {
        public string Dni { get; set; }
        public string Nombre { get; set; }
    }
    public class ClaveModel
    {
        public string Dni { get; set; }
        public string Clave { get; set; }
    }
    public class SaldoModel
    {
        public string Dni { get; set; }
        public double Saldo { get; set; }
    }
    public class SueldoModel
    {
        public string Dni { get; set; }
        public double Sueldo { get; set; }
    }

    public class MovimientoModel
    {
        public string Dni { get; set; }
        public Movimiento Movimiento { get; set; }
    }

    public class Estado
    {
        public List<UsuarioModel> Usuarios { get; set; }
        public List<ClaveModel> Claves { get; set; }
        public List<SaldoModel> Saldos { get; set; }
        public List<SueldoModel> Sueldos { get; set; }
        public List<MovimientoModel> Movimientos { get; set; }
        public double SaldoCajero { get; set; }


        // Constructor:
        public Estado(List<UsuarioModel> usuarios, List<ClaveModel> claves, List<SaldoModel> saldos, List<SueldoModel> sueldos, List<MovimientoModel> movimientos, double saldoCajero)
        {
            Usuarios = usuarios;
            Claves = claves;
            Saldos = saldos;
            Sueldos = sueldos;
            Movimientos = movimientos;
            SaldoCajero = saldoCajero;
        }

        // Constructor no parametizado
        public Estado () {}
    }

}