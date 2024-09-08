namespace Solucion;

public record SolicitudAltaUsuario
(
    Documento Dni_Administrador, 
    string Clave_Administrador,
    Documento Dni, 
    string Clave, 
    string Nombre, 
    ImportePositivo Sueldo, 
    Importe Saldo
);
