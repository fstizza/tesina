namespace Solucion;

public record PoliticaExtracciones (
    byte CantidadMaximaExtraccionesDiarias = 3,
    byte PorcentajeDelSalarioMaximoPorExtraccion = 50
);
