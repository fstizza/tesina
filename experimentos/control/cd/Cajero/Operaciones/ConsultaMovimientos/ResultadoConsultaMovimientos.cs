using System.Collections.Generic;

namespace Solucion;

public record ResultadoConsultaMovimientos
(
    bool OperacionExitosa, 
    IEnumerable<Movimiento> Movimientos, 
    string Codigo, 
    string Mensaje
    
) : ResultadoOperacion(OperacionExitosa, Codigo, Mensaje);

