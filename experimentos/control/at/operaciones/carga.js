// valida que el monto sea estrictamente positivo.
function validar_monto(monto) {
  if (monto > 0) return true
  return false
}
// actualiza los fondos del cajero (estado) con los fondos actuales mas el monto nuevo.
export function carga(e, dniAdmin, claveAdmin, monto) {
  monto = Number(monto);
  if (e.admin.dni === dniAdmin && e.admin.clave === claveAdmin && validar_monto(monto)) {
    e.fondos = e.fondos + monto
    console.log("Carga realizada con éxito")
  }
  else console.log("Carga no realizada")
  return e
}