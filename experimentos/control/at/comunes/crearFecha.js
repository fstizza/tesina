export function crearFecha() {
  let fecha = new Date()
  return [fecha.getDate(), fecha.getMonth() + 1, fecha.getFullYear()]
}