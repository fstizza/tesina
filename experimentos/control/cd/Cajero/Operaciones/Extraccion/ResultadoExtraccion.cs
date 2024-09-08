namespace Solucion;

public record ResultadoExtraccion
(
    bool OperacionExitosa, 
    string Codigo, 
    string Mensaje
    
) : ResultadoOperacion(OperacionExitosa, Codigo, Mensaje);
