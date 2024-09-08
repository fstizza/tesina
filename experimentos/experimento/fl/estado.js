import { readFileSync, writeFileSync, existsSync } from "fs";
import { nombreAdministrador, claveAdministrador, administrador } from './constantes.js';

/** Modelo que representa el estado del sistema. */
export class Estado {
  usuarios;
  claves;
  saldos;
  sueldos;
  movimientos;
  saldo;

  constructor(usuarios, claves, saldos, sueldos, movimientos, saldo) {
    this.usuarios = usuarios;
    this.claves = claves;
    this.saldos = saldos;
    this.sueldos = sueldos;
    this.movimientos = movimientos;
    this.saldo = saldo;
  }

  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
    json["usuarios"] = this.usuarios;
    json["claves"] = this.claves;
    json["saldos"] = this.saldos;
    json["sueldos"] = this.sueldos;
    json["movimientos"] = this.movimientos;
    json["saldo"] = this.saldo;
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

    estado.usuarios = [];
    estado.claves = [];
    estado.saldos = [];
    estado.sueldos = [];
    estado.movimientos = [];
    estado.saldo = 0;
    return estado;
  }
}