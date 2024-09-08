import { Estado } from './estado.js';

const Operacion = {
  extraccion : "extraccion",
  clave : "clave"
};

export class Cajero {
  constructor() {
    this.#estado = Estado.cargar();
  }

  cerrar() {
    this.#estado.guardar();
  }

  extraccion(dni, clave, monto) {
    if (!this.#estado.cuentas.has(dni)) {
      console.log("usuarioInexistente");
      return;
    }

    let cuenta = this.#estado.cuentas.get(dni);

    if (cuenta.clave !== clave) {
      console.log("claveIncorrecta");
      return;
    }

    const ahora = new Date();
    const extracciones_hoy = cuenta.movimientos.filter((item) => {
      const fechahora = new Date(item.fechahora);
      return item.operacion === Operacion.extraccion &&
        fechahora.getYear() === ahora.getYear() &&
        fechahora.getMonth() == ahora.getMonth() &&
        fechahora.getDay() === ahora.getDay();
    });

    if (extracciones_hoy.length > 2) {
      console.log("noCumplePoliticaExtraccion");
      return;
    }

    if (monto > cuenta.sueldo / 2) {
      console.log("noCumplePoliticaExtraccion2");
      return;
    }

    if (monto > this.#estado.saldo) {
      console.log("saldoInsuficiente");
      return;
    }

    if (monto > this.#estado.saldo) {
      console.log("saldoCajeroInsuficiente");
      return;
    }

    this.#estado.saldo -= monto;
    cuenta.saldo -= monto;
    cuenta.movimientos.push({fechahora: ahora, operacion : Operacion.extraccion});
    this.#estado.cuentas.set(dni, cuenta);

    console.log("ok");
  }

  cambioClave(dni, claveActual, claveNueva) {
    if (!this.#estado.cuentas.has(dni)) {
      console.log("usuarioInexistente");
      return;
    }

    let cuenta = this.#estado.cuentas.get(dni);

    if (cuenta.clave !== claveActual) {
      console.log("claveIncorrecta");
      return;
    }

    const ahora = new Date();
    const cambio_clave_mes_corriente = cuenta.movimientos.filter((item) => {
      const fechahora = new Date(item.fechahora);
      return item.operacion === Operacion.clave &&
        fechahora.getYear() === ahora.getYear() &&
        fechahora.getMonth() === ahora.getMonth();
    });

    console.log(cambio_clave_mes_corriente.length);

    if (cambio_clave_mes_corriente.length > 0) {
      console.log("cambioDeClaveBloqueado");
      return;
    }
    
    if (claveNueva.length < this.#long_min_clave) {
      console.log("noCumpleRequisitosClave1");
      return;
    }

    if (!this.#alfanumerica(claveNueva)) {
      console.log("noCumpleRequisitosClave2");
      return;
    }
  
    cuenta.clave = claveNueva;
    cuenta.movimientos.push({fechahora: ahora, operacion : Operacion.clave});
    this.#estado.cuentas.set(dni, cuenta);

    console.log("ok");
  }

  consultaSaldo(dni, clave) {
    if (!this.#estado.cuentas.has(dni)) {
      console.log("usuarioInexistente");
      return;
    }

    let cuenta = this.#estado.cuentas.get(dni);

    if (cuenta.clave !== clave) {
      console.log("claveIncorrecta");
      return;
    }

    console.log(cuenta.saldo);

    console.log("ok");
  }

  altaUsuario(dniAdmin, claveAdmin, dni, clave, nombre, sueldo, saldo) {
    if (dniAdmin !== this.#dni_admin) {
      console.log("usuarioNoHabilitado");
      return;
    }

    if (claveAdmin !== this.#clave_admin) {
      console.log("claveIncorrecta");
      return;
    }

    if (this.#estado.cuentas.has(dni)) {
      console.log("usuarioYaExistente");
      return;
    }
    
    if (this.#estado.cuentas.size >= this.#cant_max_usuarios) {
      console.log("limiteUsuariosAlcanzado");
      return;
    }

    this.#estado.cuentas.set(dni, {clave, nombre, sueldo, saldo, movimientos:[]});

    console.log("ok");
  }

  carga(dni, clave, saldo) {
    if (dni !== this.#dni_admin) {
      console.log("usuarioNoHabilitado");
      return;
    }

    if (clave !== this.#clave_admin) {
      console.log("claveIncorrecta")
      return;
    }

    this.#estado.saldo += saldo;

    console.log("ok");
  }

  consultaMovimientos(dniAdmin, claveAdmin, dniConsulta, desde, hasta) { 
    // Usuario no habilitado.
    if (dniAdmin !== this.#dni_admin) {
      console.log("usuarioNoHabilitado");
      return;
    }

    // Usuario inexistente.
    if (!this.#estado.cuentas.has(dniConsulta)) {
      console.log("usuarioInexistente");
      return;
    }

    // Clave incorrecta.
    if (this.#clave_admin !== claveAdmin) {
      console.log("claveIncorrecta");
      return;
    }
    
    desde = new Date(desde);
    hasta = new Date(hasta);
    const movimientos_desde_hasta = this.#estado.cuentas.get(dniConsulta).movimientos.filter((item) => {
      return desde <= item.fechahora <= hasta;
    });

    console.log(movimientos_desde_hasta);

    console.log("ok");
  }

  #alfanumerica(clave) {
    const alfanum = /^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$/;
    return alfanum.exec(clave).length !== 0;
  }


  #estado;
  #cant_max_usuarios = 5;
  #long_min_clave = 8;
  #dni_admin = "40000000";
  #nombre_admin = "Admin";
  #clave_admin = "ClaveAdmin";
}
