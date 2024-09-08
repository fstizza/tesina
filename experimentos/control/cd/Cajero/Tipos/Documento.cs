using System;

namespace Solucion;

public record Documento 
{
    public Documento(int numero)
    {
        if (numero < 1 || numero > 99999999)
        {
            throw new Exception($"Documento inválido: {numero}.");
        }

        Numero = numero;
    }

    public static Documento Parsear(string arg)
    {
        if (int.TryParse(arg, out var numero))
        {
            return new Documento(numero);
        }
        else
        {
            throw new Exception($"Documento inválido: {arg}.");
        }
    }

    public int Numero { get; }

    public static implicit operator int(Documento d) => d.Numero;

    public static implicit operator Documento(int numero) => new(numero);

    public static implicit operator Documento(string arg) => Parsear(arg);
}
