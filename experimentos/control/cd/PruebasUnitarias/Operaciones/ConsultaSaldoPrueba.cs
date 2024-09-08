namespace Solucion.PruebasUnitarias;

public class ConsultaSaldoPrueba
{
    private readonly Usuario _usuario;
    private readonly UsuariosMock _usuariosMock;
    private readonly Mock<IMovimientos> _movimientosMock;
    private readonly decimal _saldoCuenta;
    private readonly ConsultaSaldo _consultaSaldo;
    private readonly SolicitudConsultaSaldo _solicitudConsultaSaldo;

    public ConsultaSaldoPrueba()
    {
        _usuario = UsuarioFactoria.Crear();
        _usuariosMock = new UsuariosMock();
        _usuariosMock.Configurar(_usuario.NumeroDocumento, _usuario);

        _solicitudConsultaSaldo = new SolicitudConsultaSaldo(_usuario.NumeroDocumento, "ABC");

        _movimientosMock = new Mock<IMovimientos>();
        _saldoCuenta = 5000;
        _movimientosMock
            .Setup(o => o.ObtenerSaldoActualCuenta(_usuario))
            .Returns(_saldoCuenta);

        _consultaSaldo = new ConsultaSaldo(_usuariosMock.Object, _movimientosMock.Object);
    }

    [Fact]
    public void UsuarioNoAutenticado_OperacionNoExitosa()
    {
        _usuariosMock
            .Setup(o => o.AutenticarUsuario(_solicitudConsultaSaldo.Dni, _solicitudConsultaSaldo.Clave))
            .Returns(new ResultadoAutenticarUsuario(null));

        var resultado = _consultaSaldo.Ejecutar(_solicitudConsultaSaldo);

        Assert.False(resultado.OperacionExitosa);
    }

    [Fact]
    public void UsuarioAutenticado_OperacionExitosa()
    {
        var resultado = _consultaSaldo.Ejecutar(_solicitudConsultaSaldo);

        Assert.True(resultado.OperacionExitosa);
        Assert.Equal(_saldoCuenta, resultado.Saldo);
    }
}

