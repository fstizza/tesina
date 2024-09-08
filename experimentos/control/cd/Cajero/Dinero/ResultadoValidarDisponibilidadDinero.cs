namespace Solucion
{
    public record ResultadoValidarDisponibilidadDinero(
        bool Disponible, string Codigo = null, string MensajeError = null);
}
