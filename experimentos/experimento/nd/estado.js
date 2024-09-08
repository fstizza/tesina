import { readFileSync, writeFileSync, existsSync } from "fs";

/** Modelo que representa el estado del sistema. */
export class Estado {
  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
    json.cuentas = Object.fromEntries(this.cuentas);
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
      let estado = new Estado();
      let json = JSON.parse(contenido);
      estado.cuentas = new Map(Object.entries(json["cuentas"]));
      estado.saldo = json["saldo"];
      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    return estado;
  }

  cuentas = new Map();
  saldo = 0;
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
