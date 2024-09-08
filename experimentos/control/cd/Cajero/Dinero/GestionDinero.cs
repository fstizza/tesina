using System;

namespace Solucion
{
    public class GestionDinero : IGestionDinero
    {
        private readonly IEstadoDinero _estado;

        public GestionDinero(IEstadoDinero estado)
        {
            _estado = estado;
        }

        public ResultadoValidarDisponibilidadDinero ValidarDisponibilidadDinero(ImportePositivo importe)
        {
            string codigoError = null, mensaje = null;
             
            var disponible = _estado.DineroDisponible >= importe.Valor;

            if (!disponible)
            {
                codigoError = "D01";
                mensaje = "El cajero no dispone de dinero suficiente para completar esta operación.";
            }

            return new ResultadoValidarDisponibilidadDinero(disponible, codigoError, mensaje);
        }

        public void Entregar(ImportePositivo monto)
        {
            _estado.DineroDisponible -= monto.Valor;

            if (_estado.DineroDisponible < 0)
            {
                throw new InvalidOperationException("El cajero no dispone de dinero suficiente para completar esta operación.");
            }
        }

        public void Cargar(ImportePositivo monto)
        {
            _estado.DineroDisponible += monto.Valor;
        }
    }
}
