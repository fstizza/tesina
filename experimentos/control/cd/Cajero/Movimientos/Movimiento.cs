using System;

namespace Solucion;

public enum TiposMovimiento
{
    SaldoInicial,
    Extraccion
}

public record Movimiento
(
    int NumeroDocumentoTitular,
    DateTime Fecha,
    TiposMovimiento Tipo,
    decimal Importe  
);
