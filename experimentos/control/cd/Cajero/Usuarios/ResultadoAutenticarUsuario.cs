namespace Solucion;

public record ResultadoAutenticarUsuario 
(
    Usuario Usuario, 
    string CodigoError = null, 
    string MensajeError = null
);
