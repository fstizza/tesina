namespace Solucion;

public record SolicitudCambioClave
(
    Documento Dni, 
    string ClaveActual, 
    string ClaveNueva
);
