import { readFileSync, writeFileSync, existsSync } from "fs";

/** Modelo que representa el estado del sistema. */
export class Estado {
  constructor() {
    this.usuarios = [];
    this.cajero = { saldo: 0 };
    this.movimientos = [];
  }

  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {
      usuarios: this.usuarios,
      cajero: this.cajero,
      movimientos: this.movimientos,
    };
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
      estado.usuarios = json.usuarios || [];
      estado.cajero = json.cajero || { saldo: 0 };
      estado.movimientos = json.movimientos || [];
      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    estado.usuarios.push({
      dni: "0",
      nombre: "admin",
      clave: "admin",
      sueldo: 0,
      saldo: 0,
      admin: true,
    });
    return estado;
  }
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
