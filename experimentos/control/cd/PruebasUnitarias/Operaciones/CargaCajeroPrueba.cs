namespace Solucion.PruebasUnitarias;

public class CargaCajeroPrueba
{
    private readonly Usuario _usuarioAdministrador;
    private readonly Usuario _usuarioNoAdministrador;
    private readonly UsuariosMock _usuariosMock;
    private readonly Mock<IGestionDinero> _gestionDineroMock;
    private readonly CargaCajero _cargaCajero;
    private readonly SolicitudCargaCajero _solicitudCargaCajero;

    public CargaCajeroPrueba()
    {
        _usuarioAdministrador = UsuarioFactoria.CrearAdministrador();
        _usuarioNoAdministrador = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        
        _gestionDineroMock = new Mock<IGestionDinero>();

        _cargaCajero = new CargaCajero(
            _usuariosMock.Object, _gestionDineroMock.Object);

        _solicitudCargaCajero = new SolicitudCargaCajero(
            _usuarioAdministrador.NumeroDocumento, "ABCD1234", 25000);
    }

    [Fact]
    public void UsuarioAdministradorNoAutenticado_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, null);

        var resultado = _cargaCajero.Ejecutar(_solicitudCargaCajero);

        Assert.False(resultado.OperacionExitosa);
    }

    [Fact]
    public void UsuarioNoAdministrador_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioNoAdministrador);

        var resultado = _cargaCajero.Ejecutar(_solicitudCargaCajero);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("S02", resultado.Codigo);
    }

    [Fact]
    public void UsuarioEsAdministrador_OperacionExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioAdministrador);

        var resultado = _cargaCajero.Ejecutar(_solicitudCargaCajero);

        Assert.True(resultado.OperacionExitosa);
        Assert.Equal("RC00", resultado.Codigo);
        _gestionDineroMock.Verify(o => o.Cargar(_solicitudCargaCajero.Monto), Times.Once());
    }
}
