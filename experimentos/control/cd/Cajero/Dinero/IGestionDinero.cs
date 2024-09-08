namespace Solucion
{
    public interface IGestionDinero
    {
        ResultadoValidarDisponibilidadDinero ValidarDisponibilidadDinero(ImportePositivo importe);

        void Entregar(ImportePositivo monto);

        void Cargar(ImportePositivo monto);
    }
}
