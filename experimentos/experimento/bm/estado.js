import { readFileSync, writeFileSync, existsSync } from "fs";

const parsearMontos = (objeto) => {
  const resultado = {};

  Object.keys(objeto).forEach((dni) => {
    resultado[dni] = Number.parseFloat(objeto[dni]);
  });

  return resultado;
}

/** Modelo que representa el estado del sistema. */
export class Estado {
  static CANT_MAX_USUARIOS = 5;
  static LONG_MIN_CLAVE = 8;
  static ADMINISTRADOR = '42325945';
  static NOMBRE_ADMINISTRADOR = 'Manuel Bahamonde';
  static CLAVE_ADMINISTRADOR = 'Password1!';

  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};

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

      estado.usuarios = json.usuarios;
      estado.claves = json.claves;
      estado.saldos = parsearMontos(json.saldos);
      estado.sueldos = parsearMontos(json.sueldos);
      estado.movimientos = json.movimientos;
      estado.saldo = Number.parseFloat(json.saldo);

      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();

    estado.usuarios = {
      [this.ADMINISTRADOR]: this.NOMBRE_ADMINISTRADOR,
    };
    estado.claves = {
      [this.ADMINISTRADOR]: this.CLAVE_ADMINISTRADOR,
    };
    estado.saldos = {}
    estado.sueldos = {}
    estado.movimientos = {}
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
