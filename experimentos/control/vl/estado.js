import { readFileSync, writeFileSync, existsSync } from "fs";

/** Modelo que representa el estado del sistema. */
export class Estado {
  /** Guarda la instancia actual del modelo de Estado en el archivo `estado.json`. */
  guardar() {
    let json = {};
 
    json.usuarios = this.usuarios;
    json.dniAdmin = this.dniAdmin;
    json.claveAdmin = this.claveAdmin;
    json.saldoCajero = this.saldoCajero;

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
      estado.dniAdmin = json["dniAdmin"];
      estado.claveAdmin = json["claveAdmin"];
      estado.saldoCajero = json["saldoCajero"];

      return estado;
    }
  }
  /** Retorna una instancia del modelo de estado con sus valores iniciales. */
  static #inicial() {
    let estado = new Estado();
    estado.usuarios = [];
    estado.dniAdmin = "admin";
    estado.claveAdmin = "admin";
    estado.saldoCajero = 0;

    return estado;
  }
}