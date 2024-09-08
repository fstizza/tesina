namespace Solucion;

public enum Tipos
{
    Persona = 0,
    Cajero,
    Administrador
}

public enum CodigosError
{
    OK = 0,
    UsuarioOClaveIncorrecto,
    AdministradorIncorrecto,
    UsurioExistente,
    ClaveNoSegura,
    DatoInconsistente,
    TopeCambioClave,
    TopeCantidadUsuarios,
    SaldoInsuficiente, 
    ImporteIncorrecto ,
    ErrorDePersistencia,
    NoExiste,
    NoDefinido,
    TopeExtraccionesDiarias,
    NoHabilitado,
    TopeAdelantosMensual
}
