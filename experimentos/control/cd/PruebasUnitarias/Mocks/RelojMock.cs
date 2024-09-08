using Moq;

namespace Solucion.PruebasUnitarias;

public class RelojMock : Mock<IReloj>
{
    public RelojMock()
    {
        FechaActual = new DateTime(2023, 08, 17, 07, 30, 00);

        Setup(o => o.FechaActual).Returns(() => FechaActual);
    }

    public DateTime FechaActual { get; set; }
}
 
