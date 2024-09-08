using System;

namespace Solucion;

public record RegistroCambioClave 
(
    int Dni, 
    DateTime Fecha, 
    bool Exitoso, 
    string Motivo
);
     
 