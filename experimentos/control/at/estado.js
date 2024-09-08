import { readFileSync, writeFileSync, existsSync } from "fs";

// clase para crear objetos donde guardamos los datos de una extraccion.
export class Extraccion {
  constructor(monto, fecha) {
    this.monto = monto;
    this.fecha = fecha;
  }
}

// clase para crear objetos que guardan los datos de un cambio de contraseña.
export class CambioContr {
  constructor(antigua, nueva, fecha) {
    this.fecha = fecha
    this.antigua = antigua
    this.nueva = nueva
  }
}

// clase para crear objetos donde guardaremos los datos de los usuarios.
export class Usuario {
  constructor(dni, nombre, sueldo, clave, saldo) {
    this.dni = dni;
    this.nombre = nombre;
    this.sueldo = sueldo;
    this.clave = clave;
    this.saldo = saldo;
    this.ultCambioContr = {}; // guarda un objeto de tipo CambioContr. se inicializa vacia.
    this.extHoy = []; // será un arreglo de datos tipo Extraccion y contendrá las extracciones realizadas el dia de la fecha.
    this.movTotales = []; // será un arreglo de datos tipo Extraccion y contendrá todas las extracciones realizadas por el usuario.
  }
}

/** Modelo que representa el estado del sistema. */
export class Estado {
  admin;
  usuarios; // será un arreglo de datos tipo Usuario
  registrados; // cantidad de usuarios registrados
  fondos;
  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
    // TODO: Mapear propiedades del Estado al JSON
    // json.propiedad1 = this.propiedad1;
    json.admin = this.admin
    json.usuarios = this.usuarios
    json.registrados = this.registrados
    json.fondos = this.fondos
    writeFileSync("estado.json", JSON.stringify(json, null, 2), { encoding: "utf8" });
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
      estado.admin = json["admin"]
      estado.usuarios = json["usuarios"]
      estado.registrados = json["registrados"]
      estado.fondos = json["fondos"]
      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    // TODO: Asignar valores iniciales a las propiedades del estado, por ejemplo:
    // estado.propiedad1 = valor;
    estado.admin = { dni: "admin", clave: "admin" }
    estado.usuarios = []
    estado.registrados = 0
    estado.fondos = 0
    return estado;
  }
}

/* --- Ejemplo de uso ---
import { Estado } from './estado.js';
let e = new Estado();
...
e.guardar();
*/
