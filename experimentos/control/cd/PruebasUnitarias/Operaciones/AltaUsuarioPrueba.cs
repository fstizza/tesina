namespace Solucion.PruebasUnitarias;

public class AltaUsuarioPrueba
{
    private readonly PoliticaSeguridad _politicaSeguridad;
    private readonly Usuario _usuarioAdministrador;
    private readonly Usuario _usuarioNoAdministrador;
    private readonly UsuariosMock _usuariosMock;
    private readonly Mock<IMovimientos> _movimientosMock;
    private readonly AltaUsuario _altaUsuario;
    private readonly SolicitudAltaUsuario _solicitudAltaUsuario;


    public AltaUsuarioPrueba()
    {
        _politicaSeguridad = new PoliticaSeguridad();

        _usuarioAdministrador = UsuarioFactoria.CrearAdministrador();
        _usuarioNoAdministrador = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioAdministrador);

        _movimientosMock = new Mock<IMovimientos>();

        _altaUsuario = new AltaUsuario(
            _politicaSeguridad, _usuariosMock.Object, _movimientosMock.Object);

        _solicitudAltaUsuario = new SolicitudAltaUsuario(
            _usuarioAdministrador.NumeroDocumento, "XXX", 30123123, "cl4v3_0K!", "Fernández, Luis", 8000, 8000);
    }

    [Fact]
    public void UsuarioAdministradorNoAutenticado_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, null);

        var resultado = _altaUsuario.Ejecutar(_solicitudAltaUsuario);

        Assert.False(resultado.OperacionExitosa);
    }

    [Fact]
    public void UsuarioNoAdministrador_OperacionNoExitosa()
    {
        _usuariosMock.Configurar(_usuarioAdministrador.NumeroDocumento, _usuarioNoAdministrador);

        var resultado = _altaUsuario.Ejecutar(_solicitudAltaUsuario);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("S02", resultado.Codigo);
    }

    [Fact]
    public void UsuarioYaExiste_OperacionNoExitosa()
    {
        _usuariosMock.Setup(o => o.Existe(_solicitudAltaUsuario.Dni)).Returns(true);

        var resultado = _altaUsuario.Ejecutar(_solicitudAltaUsuario);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("AU02", resultado.Codigo);
    }

    [Theory]
    [InlineData(300)]
    [InlineData(301)]
    public void ExcedeCantidadMaximaUsuarios_OperacionNoExitosa(int cantidadUsuarios)
    {
        _usuariosMock.Setup(o => o.Cantidad).Returns(cantidadUsuarios);

        var resultado = _altaUsuario.Ejecutar(_solicitudAltaUsuario);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("AU03", resultado.Codigo);
    }

    [Fact]
    public void ClaveNoSatisfacePolitica_OperacionNoExitosa()
    {
        var solicitud = _solicitudAltaUsuario with { Clave = "XXX" };

        var resultado = _altaUsuario.Ejecutar(solicitud);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("AU04", resultado.Codigo);
    }

    [Fact]
    public void SolicitudValida_OperacionExitosa()
    {
         var resultado = _altaUsuario.Ejecutar(_solicitudAltaUsuario);

        Assert.True(resultado.OperacionExitosa);
        Assert.Equal("AU00", resultado.Codigo);
        Assert.NotNull(resultado.Usuario);
        _usuariosMock.Verify(o => o.Agregar(resultado.Usuario, _solicitudAltaUsuario.Clave), Times.Once);
        _movimientosMock.Verify(o => o.RegistrarSaldoInicial(resultado.Usuario, _solicitudAltaUsuario.Sueldo), Times.Once);
    }
}

