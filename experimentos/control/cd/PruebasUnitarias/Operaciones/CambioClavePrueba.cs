namespace Solucion.PruebasUnitarias;

public class CambioClavePrueba
{
    private readonly RelojMock _relojMock;
    private readonly PoliticaSeguridad _politicaSeguridad;
    private readonly UsuariosMock _usuariosMock;
    private readonly Usuario _usuario;
    private readonly Mock<IHistorialCambiosClave> _historialCambiosClaveMock;
    private readonly CambioClave _cambioClave;
    private readonly SolicitudCambioClave _solicitudCambioClave;

    public CambioClavePrueba()
    {
        _relojMock = new RelojMock();

        _politicaSeguridad = new PoliticaSeguridad();

        _usuario = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        _usuariosMock.Configurar(_usuario.NumeroDocumento, _usuario);

        _historialCambiosClaveMock = new Mock<IHistorialCambiosClave>();

        _cambioClave = new CambioClave(
            _relojMock.Object, _politicaSeguridad, _usuariosMock.Object, _historialCambiosClaveMock.Object);

        _solicitudCambioClave = new(_usuario.NumeroDocumento, "XXX", "ABCD1234");
    }

    [Fact]
    public void UsuarioNoAutenticado_OperacionNoExitosaRegistrada()
    {
        _usuariosMock
            .Setup(o => o.AutenticarUsuario(_solicitudCambioClave.Dni, _solicitudCambioClave.ClaveActual))
            .Returns(new ResultadoAutenticarUsuario(null));

        var resultado = _cambioClave.Ejecutar(_solicitudCambioClave);

        Assert.False(resultado.OperacionExitosa);
        _historialCambiosClaveMock.Verify(
            o => o.RegistrarIntentoCambioClave(
                _solicitudCambioClave.Dni, _relojMock.Object.FechaActual, false, It.IsAny<string>()), Times.Once);
    }

    [Fact]
    public void ExcedeCantidadCambiosDeClavePorPeriodo_OperacionNoExitosa()
    {
        _historialCambiosClaveMock
            .Setup(o => o.ObtenerCantidadCambiosClaveDesdeFecha(_usuario, It.IsAny<DateTime>()))
            .Returns(_politicaSeguridad.CambiosClave.CantidadCambiosClaveAdmitidosPorPeriodo);

        var resultado = _cambioClave.Ejecutar(_solicitudCambioClave);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("CC01", resultado.Codigo);
        _historialCambiosClaveMock.Verify(
            o => o.RegistrarIntentoCambioClave(
                _solicitudCambioClave.Dni, _relojMock.Object.FechaActual, false, It.IsAny<string>()), Times.Once);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("ABCD")]
    [InlineData("ABCDEFGH")]
    [InlineData("ABCDEFGHIJK")]
    [InlineData("1234")]
    [InlineData("12345678")]
    [InlineData("1234567890")]
    [InlineData("ABDC123")]
    [InlineData("ABD1234")]
    [InlineData("ABCD****")]
    public void NuevaClaveNoSatisfacePolitica_OperacionNoExitosa(string claveNueva)
    {
        var solicitud = _solicitudCambioClave with { ClaveNueva = claveNueva };

        var resultado = _cambioClave.Ejecutar(solicitud);

        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("CC02", resultado.Codigo);
    }

    [Fact]
    public void SolicitudCorrecta_OperacionExitosa()
    {
        var hashClaveNueva = "HASH!";

        _usuariosMock.Setup(o => o.CambiarClave(_usuario, _solicitudCambioClave.ClaveNueva, _relojMock.FechaActual))
            .Callback((Usuario usuario, string clave, DateTime fecha) =>
            {
                usuario.HashClave = hashClaveNueva;
                usuario.FechaUltimoCambioClave = fecha;
            });

        var resultado = _cambioClave.Ejecutar(_solicitudCambioClave);

        Assert.True(resultado.OperacionExitosa);
        Assert.Equal("CC00", resultado.Codigo);
        Assert.Equal(hashClaveNueva, _usuario.HashClave);
        Assert.Equal(_relojMock.FechaActual, _usuario.FechaUltimoCambioClave);
        _historialCambiosClaveMock.Verify(
                o => o.RegistrarIntentoCambioClave(
                    _solicitudCambioClave.Dni, _relojMock.Object.FechaActual, true, It.IsAny<string>()), Times.Once);
    }
}
