using System;
using System.Linq;

namespace Solucion;

public class Usuario {
    public readonly string NombreApellido;
    public decimal SueldoMensual;
    public string Clave;
    
    public Usuario(string nombreApellido, decimal sueldoMensual, string clave)
    {
        NombreApellido = nombreApellido;
        SueldoMensual = sueldoMensual;
        Clave = clave;
    }
    
    public bool ConfirmarClave(string clave) => Clave.Equals(clave);
}