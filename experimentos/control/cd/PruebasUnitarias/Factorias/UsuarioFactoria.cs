namespace Solucion.PruebasUnitarias;

public static class UsuarioFactoria
{
    public static Usuario Crear()
    {
        return new Usuario()
        {
            NombreApellido = "Juan Pérez",
            NumeroDocumento = 123456,
            SueldoMensual = 5000,
            EsAdministrador = false
        };
    }

    public static Usuario CrearAdministrador()
    {
        return new Usuario()
        {
            NombreApellido = "Juan Pérez",
            NumeroDocumento = 234567,
            EsAdministrador = true
        };
    }
}
