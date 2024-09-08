using System.ComponentModel.DataAnnotations;

namespace Solucion.PruebasUnitarias;

public class ConsultaMovimientosPrueba
{
    private readonly RelojMock _relojMock;
    private readonly Usuario _usuarioAdministrador;
    private readonly Usuario _usuarioConsulta;
    private readonly UsuariosMock _usuariosMock;
    private readonly Mock<IMovimientos> _movimientosMock;
    private readonly ConsultaMovimientos _consultaMovimientos;
    private readonly SolicitudConsultaMovimientos _solicitudConsultaMovimientos;

    public ConsultaMovimientosPrueba()
    {
        _relojMock = new();

        _usuarioAdministrador = UsuarioFactoria.CrearAdministrador();
        _usuarioConsulta = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioAdministrador);
        _usuariosMock.Configurar(_usuarioConsulta.NumeroDocumento, _usuarioConsulta);

        _movimientosMock = new Mock<IMovimientos>();

        _consultaMovimientos = new ConsultaMovimientos(
            _relojMock.Object, _usuariosMock.Object, _movimientosMock.Object);

        _solicitudConsultaMovimientos = new SolicitudConsultaMovimientos(
            _usuarioAdministrador.NumeroDocumento, "ABCD1234", 
            _usuarioConsulta.NumeroDocumento, 
            Desde: new DateOnly(2023,1,1), 
            Hasta: DateOnly.FromDateTime(_relojMock.FechaActual));
    }

    [Fact]
    public void UsuarioAdministradorNoAutenticado_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, null);

        var resultado = _consultaMovimientos.Ejecutar(_solicitudConsultaMovimientos);

        Assert.False(resultado.OperacionExitosa);
    }

    [Fact]
    public void UsuarioNoAdministrador_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioConsulta);

        var resultado = _consultaMovimientos.Ejecutar(_solicitudConsultaMovimientos);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("S02", resultado.Codigo);
    }

    [Fact]
    public void UsuarioConsultaNoExiste_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioConsulta.NumeroDocumento, null);

        var resultado = _consultaMovimientos.Ejecutar(_solicitudConsultaMovimientos);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("CM01", resultado.Codigo);
    }

    [Fact]
    public void FechaHastaAnteriorADesde_OperacionNoExitosa()
    {
        var solicitud = _solicitudConsultaMovimientos with 
        { 
            Hasta = _solicitudConsultaMovimientos.Desde.AddDays(-1) 
        };

        var resultado = _consultaMovimientos.Ejecutar(solicitud);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("CM02", resultado.Codigo);
    }

    [Fact]
    public void FechaHastaPosteriorHoy_OperacionNoExitosa()
    {
        var solicitud = _solicitudConsultaMovimientos with
        {
            Hasta = DateOnly.FromDateTime(_relojMock.FechaActual).AddDays(1)
        };

        var resultado = _consultaMovimientos.Ejecutar(solicitud);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("CM03", resultado.Codigo);
    }

    [Fact]
    public void SolicitudCorrecta_OperacionExitosa()
    {
        var resultado = _consultaMovimientos.Ejecutar(_solicitudConsultaMovimientos);

        Assert.True(resultado.OperacionExitosa);
        Assert.Equal("CM00", resultado.Codigo);
        _movimientosMock.Verify(o => o.ObtenerMovimientosPorFecha(
            _usuarioConsulta, _solicitudConsultaMovimientos.Desde, _solicitudConsultaMovimientos.Hasta), Times.Once);
    }
}

