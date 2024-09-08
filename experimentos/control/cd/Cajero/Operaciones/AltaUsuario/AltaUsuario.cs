using System;

namespace Solucion;

public class AltaUsuario : Operacion
{
    private readonly PoliticaSeguridad _politicaSeguridad;
    private readonly IUsuarios _usuarios;
    private readonly IMovimientos _movimientos;

    public AltaUsuario(
        PoliticaSeguridad politicaSeguridad,
        IUsuarios usuarios,
        IMovimientos movimientos) : base(usuarios)
    {
        _politicaSeguridad = politicaSeguridad;
        _usuarios = usuarios;
        _movimientos = movimientos;
    }

    public ResultadoAltaUsuario Ejecutar(SolicitudAltaUsuario solicitud)
    {
        ArgumentNullException.ThrowIfNull(solicitud);

        ResultadoAltaUsuario resultado;

        if (UsuarioNoAutenticado(solicitud.Dni_Administrador, solicitud.Clave_Administrador, out var usuarioAdministrador, out var codigo, out var mensaje) ||
            UsuarioNoEsAdministrador(usuarioAdministrador, out codigo, out mensaje) ||
            UsuarioYaExiste(solicitud.Dni, out codigo, out mensaje) ||
            ExcedeCantidadMaximaUsuarios(out codigo, out mensaje) ||
            ClaveNoSatisfacePolitica(solicitud.Clave, out codigo, out mensaje))
        {
            resultado = new ResultadoAltaUsuario(false, null, null, codigo, mensaje);
        }
        else
        {
            var usuario = new Usuario()
            {
                NombreApellido = solicitud.Nombre,
                NumeroDocumento = solicitud.Dni,
                SueldoMensual = solicitud.Sueldo,
                EsAdministrador = false
            }; 

            _usuarios.Agregar(usuario, solicitud.Clave);

            var movimientoSaldoInicial = _movimientos.RegistrarSaldoInicial(usuario, usuario.SueldoMensual);

            resultado = new ResultadoAltaUsuario(true, usuario, movimientoSaldoInicial, "AU00", "Se dio de alta el usuario exitosamente.");
        }

        return resultado;
    }
        
    private bool UsuarioYaExiste(Documento dni, out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        bool existe = _usuarios.Existe(dni);

        if (existe)
        {
            codigo = "AU02";
            mensaje = "Ya existe un usuario con ese DNI.";
        }

        return existe;
    }

    private bool ExcedeCantidadMaximaUsuarios(out string codigo, out string mensaje)
    {
        codigo = mensaje = null;

        var excede = _usuarios.Cantidad >= _politicaSeguridad.CantidadMaximaUsuarios;

        if (excede)
        {
            codigo = "AU03";
            mensaje = "Este cajero ya no permite más altas de usuarios.";
        }

        return excede;
    }

    private bool ClaveNoSatisfacePolitica(string clave, out string codigo, out string mensaje)
    {
        codigo = null;

        var satisface = _politicaSeguridad.ComplejidadClave.EsSatisfecha(clave, out mensaje);

        if (!satisface)
        {
            codigo = "AU04";
        }

        return !satisface;
    }
}
