import { obtenerUsuario} from '../comunes/obtenerUsuario.js' 


// imprime el saldo del usuario
export function saldo(e, dni, clave) {
  dni = Number(dni)
  let usuario = obtenerUsuario(e, dni);
  if (usuario && usuario.clave === clave) {
    console.log("su saldo es: ", usuario.saldo);
  }
  else console.log("no es posible imprimir su saldo.")
}