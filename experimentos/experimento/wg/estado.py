import exception as ex

from enum import Enum
from datetime import datetime
from json import dump, loads
from os.path import exists


class Operacion(Enum):
    extraccion = 0
    clave = 1


class Estado:
    """Modelo que representa el estado del sistema."""

    LONG_MIN_CLAVE = 8
    CANT_MAX_USUARIOS = 5

    def __init__(self):
        self.__DNI_ADMIN = 0
        self.__USR_ADMIN = "usr_admin"
        self.__CLAVE_ADMIN = "clave_admin"
        self.usuarios = {self.__DNI_ADMIN: self.__USR_ADMIN}
        self.claves = {self.__DNI_ADMIN: self.__CLAVE_ADMIN}
        self.movimientos = {}
        self.saldos = {}
        self.sueldos = {}
        self.saldo = 0

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["usuarios"] = self.usuarios
        json["claves"] = self.claves
        movimientos = {}
        for dni, movs in self.movimientos.items():
            movimientos[dni] = list(map(lambda m: (m[0].timestamp(), m[1].value), movs))

        json["movimientos"] = movimientos
        json["saldos"] = self.saldos
        json["sueldos"] = self.sueldos
        json["saldo"] = self.saldo
        with open("estado.json", "w") as estado_archivo:
            dump(json, estado_archivo)

    @classmethod
    def cargar(cls):
        """Retorna una instancia del modelo de estado con los valores guardados en `estado.json`."""
        contenido = ""
        if exists("estado.json"):
            with open("estado.json", "r") as estado_archivo:
                contenido = estado_archivo.read()
        if contenido != "":
            json = loads(contenido)
            estado = cls()
            estado.usuarios = json["usuarios"]
            estado.claves = json["claves"]
            movimientos = {}
            for dni, movs in json["movimientos"].items():
                movimientos[dni] = list(
                    map(
                        lambda m: (
                            datetime.fromtimestamp(m[0]),
                            Operacion.extraccion if m[1] == 0 else Operacion.clave,
                        ),
                        movs,
                    )
                )

            estado.movimientos = movimientos
            estado.saldos = json["saldos"]
            estado.sueldos = json["sueldos"]
            estado.saldo = json["saldo"]

            # Esto es un asco pero quiero que mis keys sean int.
            estado.usuarios = {int(k): v for k, v in estado.usuarios.items()}
            estado.claves = {int(k): v for k, v in estado.claves.items()}
            estado.movimientos = {int(k): v for k, v in estado.movimientos.items()}
            estado.saldos = {int(k): v for k, v in estado.saldos.items()}
            estado.sueldos = {int(k): v for k, v in estado.sueldos.items()}
            return estado
        else:
            return Estado.__inicial()

    @classmethod
    def __inicial(cls):
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = cls()
        return estado

    def __persist(self, fun, *args):
        fun(*args)
        self.guardar()

    def __verificar_cred(self, dni, clave):
        if dni not in self.usuarios:
            raise ex.UsuarioInexistente()

        if self.claves[dni] != clave:
            raise ex.ClaveIncorrecta()

    def __verificar_admin(self, dni_adm, clave_adm):
        if dni_adm != self.__DNI_ADMIN:
            raise ex.UsuarioNoHabilitado

        if clave_adm != self.claves[dni_adm]:
            raise ex.ClaveIncorrecta

    def __alta_usuario(self, dni_adm, clave_adm, dni, clave, nombre, sueldo, saldo):
        self.__verificar_admin(dni_adm, clave_adm)

        if dni in self.usuarios:
            raise ex.UsuarioYaExistente

        if len(self.usuarios) >= self.CANT_MAX_USUARIOS:
            ex.LimiteUsuariosAlcanzado

        self.usuarios[dni] = nombre
        self.claves[dni] = clave
        self.movimientos[dni] = []
        self.saldos[dni] = saldo
        self.sueldos[dni] = sueldo

    def __cambio_clave(self, dni, clave, nueva_clave):
        self.__verificar_cred(dni, clave)

        ahora = datetime.now()
        clave_prev = [mv for mv in self.movimientos[dni] if mv[1] == Operacion.clave]
        clave_mes = [
            cl
            for cl in clave_prev
            if (cl[0].month, cl[0].year) == (ahora.month, ahora.year)
        ]
        if clave_mes:
            raise ex.CambioDeClaveBloqueado()

        if len(nueva_clave) < self.LONG_MIN_CLAVE:
            raise ex.NoCumpleRequisitosClave()

        if not nueva_clave.isalnum():
            raise ex.NoCumpleRequisitosClave()

        self.claves[dni] = nueva_clave
        self.movimientos[dni].append((ahora, Operacion.clave))

    def __carga(self, dni, clave, monto):
        self.__verificar_admin(dni, clave)
        self.saldo += monto

    def __extraccion(self, dni, clave, monto):
        self.__verificar_cred(dni, clave)

        ahora = datetime.now()
        extr_prev = [
            mv for mv in self.movimientos[dni] if mv[1] == Operacion.extraccion
        ]
        extr_dia = [ex for ex in extr_prev if ex[0].date() == ahora.date()]
        if len(extr_dia) > 2:
            raise ex.NoCumplePoliticaExtraccion()

        if monto > self.sueldos[dni] // 2:
            raise ex.NoCumplePoliticaExtraccion()

        if self.saldos[dni] < monto:
            raise ex.SaldoInsuficiente()

        if self.saldo < monto:
            raise ex.SaldoCajeroInsuficiente()

        self.saldos[dni] -= monto
        self.saldo -= monto
        self.movimientos[dni].append((ahora, Operacion.extraccion))

    def alta_usuario(self, dni_adm, clave_adm, dni, clave, nombre, sueldo, saldo):
        self.__persist(
            self.__alta_usuario, dni_adm, clave_adm, dni, clave, nombre, sueldo, saldo
        )

    def cambio_clave(self, dni, clave, nueva_clave):
        self.__persist(self.__cambio_clave, dni, clave, nueva_clave)

    def carga(self, dni, clave, monto):
        self.__persist(self.__carga, dni, clave, monto)

    def consulta_movimientos(self, dni_adm, clave_adm, dni_consulta, desde, hasta):
        self.__verificar_admin(dni_adm, clave_adm)

        if dni_consulta not in self.usuarios:
            raise ex.UsuarioInexistente

        mov = [
            m
            for m in self.movimientos[dni_consulta]
            if desde.date() <= m[0].date() and m[0].date() <= hasta.date()
        ]

        print("Fecha     |     Operacion")
        for fecha, op in mov:
            print(f"{fecha}|{op}")

    def consulta_saldo(self, dni, clave):
        self.__verificar_cred(dni, clave)
        print(self.saldos[dni])

    def extraccion(self, dni, clave, monto):
        self.__persist(self.__extraccion, dni, clave, monto)


""" --- Ejemplo de uso ---
from estado import Estado

e = Estado.cargar();
...
e.guardar();
"""
