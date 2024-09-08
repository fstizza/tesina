import { readFileSync, writeFileSync, existsSync } from "fs";
import { ATM } from "./atm.js";
import { Manager } from "./manager.js";

/** Modelo que representa el estado del sistema.
 * @class
 */
export class Estado {
  /**
   * @type {Manager} manager
   */
  manager

  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    writeFileSync("estado.json", JSON.stringify(this.manager), { encoding: "utf8" });
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
      const json = JSON.parse(contenido)
      const estado = new Estado()
      estado.manager = Manager.fromObject(json)
      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    estado.manager = new Manager(new ATM(), {}, {})
    return estado;
  }
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
