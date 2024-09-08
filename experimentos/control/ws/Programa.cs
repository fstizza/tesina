using System;
using System.Linq;

namespace Solucion;

public class Programa
{
    public static void Main(string[] args)
    {
        if (!args.Any())
        {
            Console.WriteLine("Sin argumentos.");
            Environment.Exit(1);
        }

        switch (args[0])
        {
            case "extraccion":
                Extraer(args);
                break;
            case "clave":
                CambiarClave(args);
                break;
            case "saldo":
                ConsultarSaldo(args);
                break;
            case "alta":
                AltaUsuario(args);
                break;
            case "carga":
                CargaCajero(args);
                break;
            case "movimientos":
                Movimientos(args);
                break;
            default:
                Console.WriteLine("Operación inválida.");
                Environment.Exit(1);
                break;
        }
    }
    
    private static bool AutenticarUsuario(Estado estado, string documento, string clave)
    {
        var existe = estado.Usuarios.TryGetValue(documento, out var usuario);
        if (!existe) return false;
        return usuario.ConfirmarClave(clave);
    }
    
    private static bool EsAdmin(Estado estado, string documento) => estado.UsuariosAdmin.Contains(documento);
    
    public static bool Extraer(Estado estado, string documento, string clave, decimal monto)
    {
        if (!AutenticarUsuario(estado, documento, clave)) { Console.WriteLine("No se pudo autenticar al usuario."); return false; }
        if (monto <= 0) { Console.WriteLine("El monto a extraer no puede ser negativo o nulo."); return false; }
        if (estado.SaldoCajero < monto) { Console.WriteLine($"El cajero solo cuenta con saldo de {estado.SaldoCajero}."); return false; }

        /* Inicio sección de posibles cambios */
        var usuario = estado.Usuarios[documento];
        if (monto * 2 > usuario.SueldoMensual) { Console.WriteLine("El monto a extraer supera la mitad del sueldo mensual del usuario."); return false; }

        var hoy = DateOnly.FromDateTime(DateTime.Now);
        // Busco todos los movimientos que pertenezcan al usuario en este día y que sean negativos (extracciones)
        var extraccionesHoy = estado.HistoricoMovimientos.FindAll(m => m.DocumentoUsuario == documento && m.Fecha == hoy && m.Monto < 0).Count;
        if (extraccionesHoy >= 3) { Console.WriteLine("El usuario ya realizó 3 extracciones el día de hoy."); return false; }
        /* Fin sección de posibles cambios */
        
        var saldo = estado.SaldosUsuarios[documento];
        var newSaldo = saldo - monto;
        if (newSaldo < 0) { Console.WriteLine("El usuario no cuenta con los fondos suficiente para realizar esta extracción."); return false; }

        estado.SaldosUsuarios[documento] = newSaldo;
        var movimiento = new MovimientoCaja() { Fecha = hoy, DocumentoUsuario = documento, Monto = -monto };
        estado.HistoricoMovimientos.Add(movimiento);
        return true;
    }
    
    private static void Extraer(string[] args)
    {
        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación extraccion"); return; }
        var estado = Estado.Cargar();
        
        var documento = args[1];
        var password = args[2];
        var montoString = args[3];
        var monto = Decimal.Parse(montoString);
        var exito = Extraer(estado, documento, password, monto);
        Console.WriteLine(exito
            ? $"Se extrajo {monto} de la cuenta del usuario {documento}"
            : "No se pudo completar la operación");
        estado.Guardar();
    }
    
    private static bool CambiarClave(Estado estado, string documento, string clave, string nuevaClave)
    {
        if (!AutenticarUsuario(estado, documento, clave)) { Console.WriteLine("No se pudo autenticar al usuario."); return false; }
        if (nuevaClave.Length < 8) { Console.WriteLine("La nueva clave debe contener al menos 8 caracteres."); return false; }
        if (!nuevaClave.Any(Char.IsLetter) || !nuevaClave.Any(Char.IsDigit)) { Console.WriteLine("La nueva clave debe contener al menos 1 letra y 1 numero."); return false; }
        
        /* Inicio sección de posibles cambios */
        var hoy = DateOnly.FromDateTime(DateTime.Now);
        var ultimoCambio = estado.HistoricoClaves.FindLast(c => c.DocumentoUsuario == documento);
        if (ultimoCambio != null)
        {
            var fecha = ultimoCambio.Fecha.AddMonths(1);
            var mesSiguiente = new DateOnly(fecha.Year, fecha.Month, 1);
            if (hoy < mesSiguiente) { Console.WriteLine("El usuario ya realizó un cambio de clave este mes."); return false; }
        }
        /* Fin sección de posibles cambios */
        
        var usuario = estado.Usuarios[documento];
        usuario.Clave = clave;
        var cambio = new CambioPassword() { DocumentoUsuario = documento, Fecha = hoy };
        estado.HistoricoClaves.Add(cambio);
        return true;
    }
    
    private static void CambiarClave(string[] args)
    {
        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación clave"); return; }
        var estado = Estado.Cargar();
        
        var documento = args[1];
        var claveActual = args[2];
        var nuevaClave = args[3];
        var exito = CambiarClave(estado, documento, claveActual, nuevaClave);
        Console.WriteLine(exito
            ? $"La clave del usuario {documento}, se cambio satisfactoriamente"
            : "No se pudo completar la operación");
        estado.Guardar();
    }
    
    private static bool ConsultarSaldo(Estado estado, string documento, string clave, out decimal saldo)
    {
        if (!AutenticarUsuario(estado, documento, clave)) { Console.WriteLine("No se pudo autenticar al usuario."); saldo = 0; return false; }
        saldo = estado.SaldosUsuarios[documento];
        return true;
    }
    
    private static void ConsultarSaldo(string[] args)
    {
        if (args.Length < 3) { Console.WriteLine("Faltan argumentos para la operación saldo"); return; }
        var estado = Estado.Cargar();

        var documento = args[1];
        var clave = args[2];
        var exito = ConsultarSaldo(estado, documento, clave, out var saldo);
        Console.WriteLine(exito
            ? $"El usuario {documento} tiene saldo: ${saldo}"
            : "No se pudo completar la operación");
        // No es necesario guardar porque esta operación no modifica nada
        //estado.Guardar();
    }
    
    private static bool AltaUsuario(Estado estado, string documentoAdmin, string claveAdmin, string documento, string clave, string nombre, decimal sueldo)
    {
        if (!AutenticarUsuario(estado, documentoAdmin, claveAdmin)) { Console.WriteLine("No se pudo autenticar al usuario."); return false; }
        if (!EsAdmin(estado, documentoAdmin)) { Console.WriteLine("El usuario de la operación no es administrador."); return false; }
        var existe = estado.Usuarios.ContainsKey(documento);
        if (existe) { Console.WriteLine("Ya existe un usuario con ese documento."); return false; }
        
        /* Inicio sección de posibles cambios */
        const int MAXIMO_USUARIOS = 5;
        if (estado.Usuarios.Count >= MAXIMO_USUARIOS) { Console.WriteLine("El sistema llegó a su máximo de usuarios."); return false; }
        /* Fin sección de posibles cambios */
        
        if (clave.Length < 8) { Console.WriteLine("La nueva clave debe contener al menos 8 caracteres."); return false; }
        if (!clave.Any(Char.IsLetter) || !clave.Any(Char.IsDigit)) { Console.WriteLine("La nueva clave debe contener al menos 1 letra y 1 numero."); return false; }
        if (sueldo <= 0) { Console.WriteLine("El sueldo mensual no puede ser negativo o nulo."); return false; }
        var usuario = new Usuario(nombre, sueldo, clave);
        estado.Usuarios.Add(documento, usuario);
        estado.SaldosUsuarios.Add(documento, sueldo);
        return true;
    }
    
    private static void AltaUsuario(string[] args)
    {
        if (args.Length < 7) { Console.WriteLine("Faltan argumentos para la operación alta"); return; }
        var estado = Estado.Cargar();
        
        var documentoAdmin = args[1];
        var claveAdmin = args[2];
        var documento = args[3];
        var clave = args[4];
        var nombre = args[5];
        var sueldo = Decimal.Parse(args[6]);
        
        var exito = AltaUsuario(estado, documentoAdmin, claveAdmin, documento, clave, nombre, sueldo);
        Console.WriteLine(exito
            ? $"Se creó el usuario {documento} exitosamente."
            : "No se pudo completar la operación");
        estado.Guardar();
    }
    
    private static bool CargaCajero(Estado estado, string documento, string clave, decimal monto)
    {
        if (!AutenticarUsuario(estado, documento, clave)) { Console.WriteLine("No se pudo autenticar al usuario."); return false; }
        if (!EsAdmin(estado, documento)) { Console.WriteLine("El usuario de la operación no es administrador."); return false; }
        if (monto <= 0) { Console.WriteLine("El monto a extraer no puede ser negativo o nulo."); return false; }
        
        estado.SaldoCajero += monto;
        return true;
    }
    
    private static void CargaCajero(string[] args)
    {
        if (args.Length < 4) { Console.WriteLine("Faltan argumentos para la operación carga"); return; }
        var estado = Estado.Cargar();
        
        var documento = args[1];
        var clave = args[2];
        var monto = Decimal.Parse(args[3]);
        
        var exito = CargaCajero(estado, documento, clave, monto);
        Console.WriteLine(exito
            ? $"Se acreditaron exitosamente ${monto} al cajero."
            : "No se pudo completar la operación");
        estado.Guardar();
    }
    
    private static bool Movimientos(Estado estado, string documento, string clave, string documentoBuscar, DateOnly desde, DateOnly hasta)
    {
        if (!AutenticarUsuario(estado, documento, clave)) { Console.WriteLine("No se pudo autenticar al usuario."); return false; }
        if (!EsAdmin(estado, documento)) { Console.WriteLine("El usuario de la operación no es administrador."); return false; }
        
        var historico = estado.HistoricoMovimientos.FindAll(m => m.DocumentoUsuario == documentoBuscar && desde <= m.Fecha && m.Fecha <= hasta);
        Console.WriteLine($"Historico de movimiento de la cuenta: {documentoBuscar}");
        Console.WriteLine("----------------------------");
        historico.ForEach(m => Console.WriteLine($"{m.Fecha} - {m.Monto}"));
        Console.WriteLine("----------------------------");
        return true;
    }
    
    private static void Movimientos(string[] args)
    {
        if (args.Length < 6) { Console.WriteLine("Faltan argumentos para la operación carga"); return; }
        var estado = Estado.Cargar();
        
        var documento = args[1];
        var clave = args[2];
        var documentoABuscar = args[3];
        var desde = DateOnly.Parse(args[4]);
        var hasta = DateOnly.Parse(args[5]);
        
        var exito = Movimientos(estado, documento, clave, documentoABuscar, desde, hasta);
        Console.WriteLine(exito
            ? $"Operación finalizada."
            : "No se pudo completar la operación");
        estado.Guardar();
    }
}
