namespace Solucion;

public record ResultadoConsultaSaldo
(
    bool OperacionExitosa, 
    decimal? Saldo, 
    string Codigo, 
    string Mensaje
    
) : ResultadoOperacion(OperacionExitosa, Codigo, Mensaje);