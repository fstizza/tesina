using System;

namespace Solucion
{
    public enum OperacionTipo
    {
        EXTRACCION,
        ADELANTO,
        CLAVE,
    }

    public partial class Resultado
    {
        public const string OK = "Operación exitosa. ";
        public const string USUARIO_INEXISTENTE = "EL USUARIO NO EXISTE";
        public const string USUARIO_YA_EXISTENTE = "EL USUARIO YA EXISTE";
        public const string CLAVE_INCORRECTA = "CLAVE INCORRECTA";
        public const string SALDO_CAJERO_INSUFICIENTE = "SALDO DEL CAJERO INSUFICIENTE";
        public const string SALDO_INSUFICIENTE = "SALDO DEL USUARIO INSUFICIENTE";
        public const string NO_CUMPLE_POLITICA_EXTRACCION = "NO SE CUMPLE CON LA POLITICA DE EXTRACCION";
        public const string NO_CUMPLE_POLITICA_EXTRACCION_ADELANTO = "NO SE CUMPLE CON LA POLITICA DE EXTRACCION DEL ADELANTO";
        public const string NO_CUMPLE_POLITICA_ADELANTO = "NO SE CUMPLE CON LA POLITICA DE ADELANTO";
        public const string LIMITE_USUARIOS_ALCANZADO = "SE ALCANZO EL LIMITE DE USUARIOS";
        public const string CAMBIO_DE_CLAVE_BLOQUEADO = "CAMBIO DE CLAVE BLOQUEADO";
        public const string USUARIO_NO_HABILITADO = "USUARIO NO HABILITADO";
        public const string NO_CUMPLE_REQUISITOS_CLAVE_1 = "LA CLAVE NO CUMPLE CON LA LONGITUD MINIMA";
        public const string NO_CUMPLE_REQUISITOS_CLAVE_2 = "LA CLAVE NO CUMPLE CON EL REQUISITO DE SER ALFANUMERICA";
    }

    public class Movimiento
    {
        public DateTime Fecha { get; set; }
        public OperacionTipo Operacion { get; set; }
    }

}

