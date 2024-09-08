import { ValidatePassword } from "./password.js";

/** Modelo que representa un usuario.
 * @class
 */
export class User {
  /**
   * @type {string} name
   */
  name;

  /**
   * @type {string} password
   */
  password;

  constructor(name, password) {
    this.name = name;
    this.password = password;
  }

  authenticate(password) {
    return this.password === password
  }

  changePassword(password) {
    if(!ValidatePassword){
        throw Error("El formato de la clave no es valido")
    }
    this.password = password
  }
}
