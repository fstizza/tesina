using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;

namespace Solucion;

public class Programa
{
    public static void Main(string[] args)
    {
        if (!args.Any())
        {
            Console.WriteLine("Sin argumentos.");
            System.Environment.Exit(1);
        }

        Estado estado = Estado.Cargar();


        string dniInput;
        string claveInput;
        string dniAdminiInput;
        string claveAdminInput;
        Sueldo sueldo;
        Saldo saldo;
        Usuario usuario;
        Clave clave;
        DateTime desde;
        DateTime hasta;

        switch (args[0])
        {
            case "extraccion":

                dniInput = args[1];
                claveInput = args[2];
                var montoIngresadoString = args[3];

                usuario = estado.Usuarios.FirstOrDefault(u => u.ValorDNI == dniInput);

                clave = estado.Claves.FirstOrDefault(u => u.ValorDNI == dniInput && u.ValorClave == claveInput);

                if (decimal.TryParse(montoIngresadoString, out decimal montoIngresado))
                {
                    saldo = estado.Saldos.FirstOrDefault(u => u.ValorDNI == dniInput);
                    sueldo = estado.Sueldos.FirstOrDefault(u => u.ValorDNI == dniInput);

                    if (usuario.ValorDNI.Any() && clave.ValorClave.Any() && saldo != null && saldo.ValorMonto >= montoIngresado)
                    {
                        var extracciones = estado.Movimientos.Count(x => x.ValorDNI == usuario.ValorDNI && x.Operacion == Operacion.Extraccion);

                        if (extracciones > 2)
                        {
                            Console.WriteLine($"{Resultados.NoCumplePoliticaExtraccion}");
                        }
                        else if (montoIngresado > ((int)(sueldo.ValorMonto / 2)))
                        {
                            Console.WriteLine($"{Resultados.NoCumplePoliticaExtraccion2}");
                        }
                        else
                        {
                            saldo.ValorMonto -= montoIngresado;
                            estado.Movimientos.Add(
                                new Movimiento
                                {
                                    FechaHora = new FechaHora() { ValorFechaHora = DateTime.Now },
                                    Operacion = Operacion.Extraccion,
                                    ValorDNI = usuario.ValorDNI,
                                }
                            );
                        }
                    }
                    else if (usuario.ValorDNI.Any() && clave.ValorClave.Any() && saldo != null && saldo.ValorMonto < montoIngresado)
                    {
                        Console.WriteLine($"{Resultados.SaldoInsuficiente}");
                    }
                }
                else
                {
                    Console.WriteLine($"{Resultados.NoCumplePoliticaExtraccion}");
                }

                if (usuario == null)
                {
                    Console.WriteLine($"{Resultados.UsuarioInexistente}");
                }

                if (usuario != null && clave == null)
                {
                    Console.WriteLine($"{Resultados.ClaveIncorrecta}");
                }

                break;
            case "clave":

                dniInput = args[1];

                var claveActual = args[2];
                var nuevaClave = args[3];

                usuario = estado.Usuarios.Where(u => u.ValorDNI == dniInput).FirstOrDefault();

                clave = estado.Claves.Where(c => c.ValorDNI == dniInput && c.ValorClave == claveActual).FirstOrDefault();

                if (usuario == null)
                {
                    Console.WriteLine($"{Resultados.UsuarioInexistente}");
                }

                if (usuario != null && clave == null)
                {
                    Console.WriteLine($"{Resultados.ClaveIncorrecta}");
                }
                else
                {
                    clave.ValorClave = nuevaClave;
                }

                //ToDo: Completar.

                break;
            case "saldo":

                dniInput = args[1];

                usuario = estado.Usuarios.Where(u => u.ValorDNI == dniInput).FirstOrDefault();

                claveInput = args[2];

                clave = estado.Claves.Where(c => c.ValorDNI == dniInput && c.ValorClave == claveInput).FirstOrDefault();

                saldo = estado.Saldos.Where(s => s.ValorDNI == dniInput).FirstOrDefault();

                if (usuario != null && clave != null && saldo != null)
                {
                    Console.WriteLine($"{Resultados.Ok} {saldo.ValorMonto}");
                }

                if (usuario != null)
                {
                    Console.WriteLine($"{Resultados.UsuarioInexistente}");
                }

                if (clave != null)
                {
                    Console.WriteLine($"{Resultados.ClaveIncorrecta}");
                }

                break;
            case "alta":

                dniAdminiInput = args[1];
                claveAdminInput = args[2];
                dniInput = args[3];
                claveInput = args[4];
                var nombreInput = args[5];
                var sueldoInput = args[6];
                var saldoInput = args[7];

                var contraseñaCorrecta = string.Equals(claveAdminInput, ConstantesGlobales.CLAVE);
                var dniCorrecto = string.Equals(dniAdminiInput, ConstantesGlobales.ADMINISTRADOR);

                usuario = estado.Usuarios.Where(u => u.ValorDNI == dniInput).FirstOrDefault();

                clave = estado.Claves.Where(c => c.ValorDNI == dniInput).FirstOrDefault();

                sueldo = estado.Sueldos.Where(s => s.ValorDNI == dniInput).FirstOrDefault();

                if (!contraseñaCorrecta || string.IsNullOrEmpty(claveAdminInput))
                {
                    Console.WriteLine(Resultados.ClaveIncorrecta);
                }

                if (!dniCorrecto || string.IsNullOrEmpty(dniAdminiInput))
                {
                    Console.WriteLine(Resultados.UsuarioNoHabilitado);
                }

                if (usuario != null)
                {
                    Console.WriteLine(Resultados.UsuarioYaExistente);
                }



                if (contraseñaCorrecta &&
                    dniCorrecto &&
                    usuario == null &&
                    clave == null &&
                    !string.IsNullOrEmpty(nombreInput) &&
                    sueldo == null
                    )
                {
                    if (decimal.TryParse(sueldoInput, out decimal montoSueldo))
                    {
                        usuario = new Usuario
                        {
                            ValorDNI = dniInput,
                            ValorNombre = nombreInput,
                        };

                        clave = new Clave
                        {
                            ValorDNI = dniInput,
                            ValorClave = claveInput,
                        };

                        sueldo = new Sueldo
                        {
                            ValorDNI = dniInput,
                            ValorMonto = montoSueldo
                        };

                        saldo = new Saldo
                        {
                            ValorDNI = dniInput,
                            ValorMonto = montoSueldo
                        };

                        estado.Usuarios.Add(usuario);
                        estado.Claves.Add(clave);
                        estado.Sueldos.Add(sueldo);
                        estado.Saldos.Add(saldo);

                        Console.WriteLine(Resultados.Ok);
                    }
                }

                break;
            case "carga":

                dniAdminiInput = args[1];
                claveAdminInput = args[2];
                var montoInput = args[3];

                if (ConstantesGlobales.ADMINISTRADOR == dniAdminiInput &&
                    ConstantesGlobales.CLAVE == claveAdminInput &&
                    decimal.TryParse(montoInput, out decimal monto) &&
                    monto > 0)
                {
                    estado.Saldo = +monto;

                    Console.WriteLine(Resultados.Ok);
                }

                if (ConstantesGlobales.ADMINISTRADOR.Equals(dniAdminiInput) || string.IsNullOrEmpty(dniAdminiInput))
                {
                    Console.WriteLine(Resultados.UsuarioNoHabilitado);
                }

                if (ConstantesGlobales.CLAVE.Equals(claveAdminInput) || string.IsNullOrEmpty(claveAdminInput))
                {
                    Console.WriteLine(Resultados.ClaveIncorrecta);
                }

                break;
            case "movimientos":
                dniAdminiInput = args[1];
                claveAdminInput = args[2];

                if (!ConstantesGlobales.ADMINISTRADOR.Equals(dniAdminiInput) || string.IsNullOrEmpty(dniAdminiInput))
                {
                    Console.WriteLine(Resultados.UsuarioNoHabilitado);
                    break;
                }

                if (!ConstantesGlobales.CLAVE.Equals(claveAdminInput) || string.IsNullOrEmpty(claveAdminInput))
                {
                    Console.WriteLine(Resultados.ClaveIncorrecta);
                    break;
                }

                dniInput = args[3];

                usuario = estado.Usuarios.FirstOrDefault(u => u.ValorDNI == dniInput);

                if (usuario == null)
                {
                    Console.WriteLine(Resultados.UsuarioInexistente);
                    return;
                }

                if (DateTime.TryParse(args[4], out desde) && DateTime.TryParse(args[5], out hasta))
                {
                    var movs = estado.Movimientos.Where(m => m.ValorDNI == usuario.ValorDNI && m.FechaHora.ValorFechaHora <= hasta && m.FechaHora.ValorFechaHora >= desde);
                    foreach (var mov in movs)
                    {
                        Console.WriteLine($"{mov.Operacion} | {mov.FechaHora.ValorFechaHora}");
                    }
                }
                else
                {
                    Console.WriteLine("Fechas invalidas");
                }


                break;
            default:
                Console.WriteLine("Operación inválida.");
                System.Environment.Exit(1);
                break;
        }

        estado.Guardar();
    }
}

public enum Resultados
{
    Ok,
    UsuarioInexistente,
    UsuarioYaExistente,
    ClaveIncorrecta,
    SaldoCajeroInsuficiente,
    SaldoInsuficiente,
    NoCumplePoliticaExtraccion,
    NoCumplePoliticaExtraccion2,
    UsuarioNoHabilitado,
    LimiteUsuariosAlcanzado,
    CambioDeClaveBloqueado,
    NoCumpleRequisitosClave1,
    NoCumpleRequisitosClave2,
}
