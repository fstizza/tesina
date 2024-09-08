using System;

namespace Solucion;

public record Importe
{
    public Importe(decimal valor)
    {
        Valor = valor;
    }

    public static Importe Parsear(string arg)
    {
        if (!decimal.TryParse(arg, out var valor))
        {
            throw new Exception($"Importe inválido: {arg}.");
        }
        
        return new Importe(valor);
    }

    public decimal Valor { get; }

    public static implicit operator decimal(Importe importe) => importe.Valor;

    public static implicit operator Importe(decimal importe) => new(importe);

    public static implicit operator Importe(string arg) => Parsear(arg);
}

public record ImportePositivo : Importe
{
    public ImportePositivo(decimal valor) : base(valor)
    {
        if (valor <= 0)
        {
            throw new Exception("El importe debe ser mayor que cero.");
        }
    }

    public static new ImportePositivo Parsear(string arg)
    {
        if (!decimal.TryParse(arg, out var valor))
        {
            throw new Exception($"Importe inválido: {arg}.");
        }

        return new ImportePositivo(valor);
    }

    public static implicit operator decimal(ImportePositivo importe) => importe.Valor;

    public static implicit operator ImportePositivo(decimal importe) => new(importe);

    public static implicit operator ImportePositivo(string arg) => Parsear(arg);
}
