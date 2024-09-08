import { readFileSync, writeFileSync, existsSync } from "fs";

/** Modelo que representa el estado del sistema. */
export class Estado {

  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
    // TODO: Mapear propiedades del Estado al JSON
    // json.propiedad1 = this.propiedad1;
    json.usuarios = this.usuarios;
    json.claves = this.claves;
    json.saldos = this.saldos;
    json.sueldos = this.sueldos;
    json.movimientos = this.movimientos;
    json.saldo = this.saldo;

    writeFileSync("estado.json", JSON.stringify(json), { encoding: "utf8" });
  }

  /** Retorna una instancia del modelo de estado con los valores guardados en `estado.json`. */
  static cargar() {
    let contenido = "";
    if (existsSync("estado.json")) {
      contenido = readFileSync("estado.json", { encoding: "utf8" }).toString();
    }

    if (contenido === "") {
      return Estado.#inicial();
    } else {
      let json = JSON.parse(contenido);
      let estado = new Estado();
      // TODO: Mapear propiedades del objeto JSON a la instancia del estado.
      // estado.propiedad1 = json["propiedad1"];

      estado.usuarios = json["usuarios"];
      estado.claves = json["claves"];
      estado.saldos = json["saldos"];
      estado.sueldos = json["sueldos"];
      estado.movimientos = json["movimientos"];
      estado.saldo = json["saldo"];

      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
    // estado.propiedad1 = valor;

    estado.usuarios = { 37041537: "Patricio" };
    estado.claves = { 37041537: "123456" };
    estado.saldos = {};
    estado.sueldos = {};
    estado.movimientos = {};
    estado.saldo = 0;

    return estado;
  }
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
