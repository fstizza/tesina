namespace Solucion;

public record SolicitudCargaCajero
(
    Documento Dni_Administrador, 
    string Clave_Administrador, 
    ImportePositivo Monto
);
