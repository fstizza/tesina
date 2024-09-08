namespace Solucion.PruebasUnitarias;

public class ExtraccionPrueba
{
    private readonly RelojMock _relojMock;
    private readonly PoliticaExtracciones _politicaExtracciones;
    private readonly UsuariosMock _usuariosMock;
    private readonly Mock<IMovimientos> _movimientosMock;
    private readonly decimal _saldoCuenta;
    private readonly Mock<IGestionDinero> _gestionDineroMock;
    private readonly Extraccion _extraccion;
    private readonly SolicitudExtraccion _solicitudExtraccion;
    private readonly Usuario _usuario;

    public ExtraccionPrueba()
    {
        _relojMock = new RelojMock();

        _politicaExtracciones = new PoliticaExtracciones();

        _usuario = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        _usuariosMock.Configurar(_usuario.NumeroDocumento, _usuario);

        _movimientosMock = new Mock<IMovimientos>();
        _saldoCuenta = 5000;
        _movimientosMock
            .Setup(o => o.ObtenerSaldoActualCuenta(_usuario))
            .Returns(_saldoCuenta);

        _gestionDineroMock = new Mock<IGestionDinero>();
        _gestionDineroMock
            .Setup(o => o.ValidarDisponibilidadDinero(It.IsAny<ImportePositivo>()))
            .Returns(new ResultadoValidarDisponibilidadDinero(true));

        _extraccion = InstanciarExtraccion(_politicaExtracciones);

        _solicitudExtraccion = new(_usuario.NumeroDocumento, "clave", _saldoCuenta / 3);
    }

    [Fact]
    public void UsuarioNoAutenticado_OperacionNoExitosa()
    {
        _usuariosMock
            .Setup(o => o.AutenticarUsuario(_solicitudExtraccion.Dni, _solicitudExtraccion.Clave))
            .Returns(new ResultadoAutenticarUsuario(null));

        var resultado = _extraccion.Ejecutar(_solicitudExtraccion);

        Assert.False(resultado.OperacionExitosa);
    }

    [Theory]
    [InlineData(0, 0, true)]
    [InlineData(0, 10, true)]
    [InlineData(1, 0, true)]
    [InlineData(1, 1, false)]
    [InlineData(1, 10, false)]
    public void ExcedeCantidadExtraccionesDiarias_OperacionNoExitosa(
        byte cantidadMaximaExtraccionesDiarias, int cantidadExtraccionesHoy, bool operacionExitosa)
    {
        var politicaExtracciones = new PoliticaExtracciones(cantidadMaximaExtraccionesDiarias);

        _movimientosMock
            .Setup(o => o.ObtenerCantidadExtraccionesPorFecha(_usuario, DateOnly.FromDateTime(_relojMock.FechaActual)))
            .Returns(cantidadExtraccionesHoy);

        var extraccion = InstanciarExtraccion(politicaExtracciones);

        var resultado = extraccion.Ejecutar(_solicitudExtraccion);
        
        Assert.Equal(operacionExitosa, resultado.OperacionExitosa);
        if (!operacionExitosa)
        {
            Assert.Equal("EX01", resultado.Codigo);
        }
    }

    [Fact]
    public void SinPorcentajeDelSalarioMaximoPorExtraccion_OperacionExitosa()
    {
        var politicaExtracciones = new PoliticaExtracciones(
            PorcentajeDelSalarioMaximoPorExtraccion: 0);

        var extraccion = InstanciarExtraccion(politicaExtracciones);

        var resultado = extraccion.Ejecutar(_solicitudExtraccion);

        Assert.True(resultado.OperacionExitosa);
    }

    [Fact]
    public void ExcedeImporteMaximoPorExtraccion_OperacionNoExitosa()
    {
        var importeMaximoExtraccion = _usuario.SueldoMensual * _politicaExtracciones.PorcentajeDelSalarioMaximoPorExtraccion / 100;
        
        var solicitud = _solicitudExtraccion with { Monto = importeMaximoExtraccion - 1 };
        Assert.True(_extraccion.Ejecutar(solicitud).OperacionExitosa);

        solicitud = _solicitudExtraccion with { Monto = importeMaximoExtraccion };
        Assert.True(_extraccion.Ejecutar(solicitud).OperacionExitosa);

        solicitud = _solicitudExtraccion with { Monto = importeMaximoExtraccion + .0001m };

        var resultado = _extraccion.Ejecutar(solicitud);
        Assert.False(resultado.OperacionExitosa);
        Assert.Equal("EX02", resultado.Codigo);
    }

    [Fact]
    public void DineroInsuficienteEnCajero_OperacionNoExitosa()
    {
        _gestionDineroMock
            .Setup(o => o.ValidarDisponibilidadDinero(It.IsAny<ImportePositivo>()))
            .Returns(new ResultadoValidarDisponibilidadDinero(false));

        var resultado = _extraccion.Ejecutar(_solicitudExtraccion);

        Assert.False(resultado.OperacionExitosa);
    }

    [Fact]
    public void ExtraccionExitosa_RegistraMovimiento()
    {
        var resultado = _extraccion.Ejecutar(_solicitudExtraccion);

        Assert.True(resultado.OperacionExitosa);
        _movimientosMock.Verify(o => o.RegistrarExtraccion(_usuario, _solicitudExtraccion.Monto));
    }

    // 

    private Extraccion InstanciarExtraccion(PoliticaExtracciones politicaExtracciones)
    {
        return new Extraccion(
            _relojMock.Object, politicaExtracciones, _usuariosMock.Object,
            _movimientosMock.Object, _gestionDineroMock.Object);
    }
}