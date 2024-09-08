namespace Solucion;

public record SolicitudExtraccion 
(
    Documento Dni, 
    string Clave, 
    ImportePositivo Monto
);
