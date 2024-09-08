import { readFileSync, writeFileSync, existsSync } from "fs";

/** Modelo que representa el estado del sistema. */
export class Estado {
  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
    // TODO: Mapear propiedades del Estado al JSON
    // json.propiedad1 = this.propiedad1;
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
      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
    // estado.propiedad1 = valor;
    return estado;
  }
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
