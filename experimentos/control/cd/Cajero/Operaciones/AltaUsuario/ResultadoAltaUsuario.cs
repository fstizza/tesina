namespace Solucion;

public record ResultadoAltaUsuario
(
    bool OperacionExitosa, 
    Usuario Usuario, 
    Movimiento MovimientoSaldoInicial, 
    string Codigo, 
    string Mensaje
 
) : ResultadoOperacion(OperacionExitosa, Codigo, Mensaje);
 