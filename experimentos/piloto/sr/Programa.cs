using System;
using System.Collections.Generic;
using Operaciones;
using Solucion;
public class Programa
{
    #region Generadadores de data dummy

    // Generar datos dummy para Usuarios
    static List<UsuarioModel> GenerarUsuariosDummy()
    {
        List<UsuarioModel> usuarios = new List<UsuarioModel>
            {
                new()  { Dni = "12345678", Nombre = "Usuario1" },
                new()  { Dni = "23456789", Nombre = "Usuario2" },
                new()  { Dni = "34567890", Nombre = "Usuario3" }
            };

        return usuarios;
    }

    // Generar datos dummy para Claves
    static List<ClaveModel> GenerarClavesDummy()
    {
        List<ClaveModel> claves = new List<ClaveModel>
            {
                new() { Dni = "12345678", Clave = "clave1" },
                new() { Dni = "23456789", Clave = "clave2" },
                new() { Dni = "34567890", Clave = "clave3" }
            };

        return claves;
    }

    // Generar datos dummy para Saldos
    static List<SaldoModel> GenerarSaldosDummy()
    {
        List<SaldoModel> saldos = new List<SaldoModel>
            {
                new() { Dni = "12345678", Saldo = 1000.0 },
                new() { Dni = "23456789", Saldo = 2000.0 },
                new() { Dni = "34567890", Saldo = 3000.0 }
            };

        return saldos;
    }

    // Generar datos dummy para Sueldos
    static List<SueldoModel> GenerarSueldosDummy()
    {
        List<SueldoModel> sueldos = new List<SueldoModel>
            {
                new() { Dni = "12345678", Sueldo = 5000.0 },
                new() { Dni = "23456789", Sueldo = 6000.0 },
                new() { Dni = "34567890", Sueldo = 7000.0 }
            };

        return sueldos;
    }

    // Generar datos dummy para Movimientos
    static List<MovimientoModel> GenerarMovimientosDummy()
    {
        List<MovimientoModel> movimientos = new List<MovimientoModel>
            {
                new() { Dni = "12345678", Movimiento = new(){Fecha = DateTime.Now,  Operacion = OperacionTipo.EXTRACCION} },
                new() { Dni = "12345678", Movimiento = new(){Fecha = DateTime.Now.AddDays(-2),  Operacion = OperacionTipo.ADELANTO} },
                new() { Dni = "12345678", Movimiento = new(){Fecha = DateTime.Now.AddDays(-1),  Operacion = OperacionTipo.EXTRACCION} },
                new() { Dni = "12345678", Movimiento = new(){Fecha = DateTime.Now.AddDays(-1),  Operacion = OperacionTipo.CLAVE} },
                new() { Dni = "23456789", Movimiento = new(){Fecha = DateTime.Now,  Operacion = OperacionTipo.CLAVE}  },
                new() { Dni = "34567890", Movimiento = new(){Fecha = DateTime.Now,  Operacion = OperacionTipo.ADELANTO}  }
            };

        return movimientos;
    }

    #endregion

    #region Generador estado inicial especificación

    static Estado GenerarEstadoInicialEspecificacion()
    {
        var estado = new Estado()
        {
            Usuarios = new List<UsuarioModel>()
            {
                new()
                {
                    Dni = Constantes.DNI_ADMINISTRADOR,
                    Nombre = Constantes.NOMBRE_ADMINISTRADOR,
                }
            },
            Claves = new List<ClaveModel>()
            {
                new()
                {
                    Dni = Constantes.DNI_ADMINISTRADOR,
                    Clave = Constantes.CLAVE_ADMINISTRADOR,
                }
            },
            Saldos = new List<SaldoModel>(),
            Sueldos = new List<SueldoModel>(),
            Movimientos = new List<MovimientoModel>(),
            SaldoCajero = 0.0,
        };

        return estado;
    }

    #endregion

    static void Main(string[] args)
    {
        // Generar datos dummy
        List<UsuarioModel> usuarios = GenerarUsuariosDummy();
        List<ClaveModel> claves = GenerarClavesDummy();
        List<SaldoModel> saldos = GenerarSaldosDummy();
        List<SueldoModel> sueldos = GenerarSueldosDummy();
        List<MovimientoModel> movimientos = GenerarMovimientosDummy();
        double saldoCajero = 10000.0; // Establecer un saldo inicial para el cajero

        // Crear instancia del estado con datos dummy
        var estadoPruebas = new Estado(usuarios, claves, saldos, sueldos, movimientos, saldoCajero);


        // Crear instancia del estado inicial solicitado en la especificación:
        //var estadoInicial = GenerarEstadoInicialEspecificacion();

        Console.WriteLine("Estado inicializado correctamente.");


        // Para probar las operaciones:
        ConsultaSaldo.Ejecutar("12345678", "Clave1!", estadoPruebas);
    }
}
