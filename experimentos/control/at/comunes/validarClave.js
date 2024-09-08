// valida que la clave tenga al menos un caracter o simbolo, al menos un numero y 8 digitos
export function validarClave(clave) {
  const regex = /^(?=.*\d)(?=.*[a-zA-Z!@#$%^&*]).{8,}$/;
  return regex.test(clave);
}