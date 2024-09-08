using System;

namespace Solucion;

public record SolicitudConsultaMovimientos
(
    Documento Dni_Administrador, 
    string Clave_Administrador,
    Documento Dni_Consulta,
    DateOnly Desde, 
    DateOnly Hasta
);
