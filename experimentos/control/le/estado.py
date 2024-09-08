import datetime
from decimal import Decimal
from json import dump, loads
from os.path import exists
from contextlib import ContextDecorator
import sys
import time
from typing import Optional
import click

from pyrsistent import (
    PRecord,
    field,
    CheckedPMap,
    CheckedPVector,
    InvariantException,
    get_in,
)


ONE_MONTH = 1 * 30 * 24 * 60 * 60  # in seconds


class Operacion(PRecord):
    """Operación en el sistema"""

    tipo = field(type=str)
    monto = field(type=int, mandatory=False)


class Operaciones(CheckedPVector):
    __type__ = Operacion


class OperacionesPorDia(CheckedPMap):
    __key_type__ = str
    __value_type__ = Operaciones
    __invariant__ = lambda _, ops: (
        len([x for x in ops if x.tipo == "Extracción"]) <= 3,
        "Demasiadas operaciones en el día",
    )


class OperacionesPorCuenta(CheckedPMap):
    __key_type__ = str
    __value_type__ = OperacionesPorDia


class Cuenta(PRecord):
    """Cuenta usuario"""

    dni = field(type=str, mandatory=True)
    nombre = field(type=str)
    # TODO: usar hashing
    password = field(type=str, mandatory=True)
    saldo = field(type=int, initial=0, invariant=lambda s: (s >= 0, "Saldo negativo"))
    sueldo = field(type=int, initial=0, invariant=lambda s: (s >= 0, "Sueldo negativo"))
    es_admin = field(type=bool, initial=False)
    ultimo_cambio_clave = field(type=int, initial=0)


class Cuentas(CheckedPMap):
    __key_type__ = str
    __value_type__ = Cuenta


class EstadoATM(PRecord):
    """Modelo que representa el estado del sistema."""

    cuentas = field(
        type=Cuentas,
        initial=Cuentas(
            {
                "11111111": Cuenta(
                    dni="11111111",
                    password="admin",
                    saldo=10000,
                    sueldo=10000,
                    es_admin=True,
                )
            },
        ),
        invariant=lambda c: (len(c) <= 5, "Demasiadas cuentas"),
    )
    historial = field(type=OperacionesPorCuenta, initial=OperacionesPorCuenta())
    saldo = field(
        type=int,
        initial=10000,
        mandatory=True,
        invariant=lambda s: (s >= 0, "Saldo negativo"),
    )


class Estado:
    """Helper para (de)serializar el estado"""

    def __init__(self, estado=None) -> None:
        self.estado: EstadoATM = estado if estado is not None else EstadoATM()
        self.rollback = False

    @property
    def saldo(self) -> Decimal:
        return Decimal(self.estado.saldo) / 100

    @saldo.setter
    def saldo(self, monto: Decimal) -> None:
        self.estado = self.estado.set(saldo=int(monto * 100))

    def registrar_operacion(
        self, cuenta: str, fecha: datetime.date, tipo: str, monto: Decimal = Decimal(0)
    ):
        fecha_rec = fecha.strftime("%Y-%m-%d")
        ops_cuenta = self.estado.historial.get(cuenta, default=OperacionesPorDia())
        ops_fecha = ops_cuenta.get(fecha_rec, default=Operaciones())
        ops_fecha = ops_fecha.append(Operacion(tipo=tipo, monto=int(monto * 100)))
        ops_cuenta = ops_cuenta.set(fecha_rec, ops_fecha)
        historial = self.estado.historial.set(cuenta, ops_cuenta)
        self.estado = self.estado.set(historial=historial)

    def login(self, dni: str, clave: str, admin: bool = False) -> bool:
        cuenta: Cuenta = self.estado.cuentas.get(dni)
        if not cuenta:
            return False
        if admin and not cuenta.es_admin:
            return False
        # TODO: usar hash y constant time comparison
        return cuenta.password == clave

    def alta(
        self, dni: str, clave: str, nombre: str, sueldo: int, admin: bool = False
    ) -> bool:
        cuenta = self.estado.cuentas.get(dni)
        if cuenta:
            return "cuenta ya existente"

        cuenta = Cuenta(
            dni=dni,
            password=clave,
            nombre=nombre,
            sueldo=int(sueldo),
            saldo=int(sueldo),
            es_admin=admin,
        )
        try:
            cuentas = self.estado.cuentas.set(dni, cuenta)
            self.estado = self.estado.set(cuentas=cuentas)
        except InvariantException as e:
            self.rollback = True
            return ", ".join(e.invariant_errors)

        return "OK"

    def obtener_saldo(self, dni: str) -> Optional[Decimal]:
        cuenta: Cuenta = self.estado.cuentas.get(dni)
        if not cuenta:
            return None

        return Decimal(cuenta.saldo) / 100

    def obtener_sueldo(self, dni: str) -> Optional[Decimal]:
        cuenta: Cuenta = self.estado.cuentas.get(dni)
        if not cuenta:
            return None

        return Decimal(cuenta.sueldo) / 100

    def cambiar_clave(self, dni, nueva_clave) -> bool:
        cuenta: Cuenta = self.estado.cuentas[dni]

        time_now = int(time.time())
        if cuenta.ultimo_cambio_clave + ONE_MONTH > time_now:
            return False

        cuenta = cuenta.set(password=nueva_clave, ultimo_cambio_clave=time_now)
        cuentas = self.estado.cuentas.set(dni, cuenta)
        self.estado = self.estado.set(cuentas=cuentas)
        self.registrar_operacion(dni, datetime.date.today(), "Cambio de clave")
        return True

    def retirar_dinero(self, dni: str, monto: Decimal) -> Optional[str]:
        cuenta: Cuenta = self.estado.cuentas.get(dni)
        if not cuenta:
            return "Cuenta inexistente"

        try:
            self.saldo -= monto
            cuenta = cuenta.set(saldo=cuenta.saldo - int(monto * 100))
            cuentas = self.estado.cuentas.set(dni, cuenta)
            self.estado = self.estado.set(cuentas=cuentas)
            self.registrar_operacion(dni, datetime.date.today(), "Extracción", monto)
        except InvariantException as e:
            self.rollback = True
            return ", ".join(e.invariant_errors)

        return "OK"

    def consultar_movimientos(
        self, dni: str, fecha: datetime.date
    ) -> Optional[Decimal]:
        fecha_rec = fecha.strftime("%Y-%m-%d")
        operaciones: Operaciones = get_in(
            [dni, fecha_rec], self.estado.historial, default=Operaciones()
        )
        return operaciones

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = self.estado.serialize()
        with open("estado.json", "w") as estado_archivo:
            dump(json, estado_archivo, indent=2)

    @staticmethod
    def cargar():
        """Retorna una instancia del modelo de estado con los valores guardados en `estado.json`."""
        contenido = ""
        if exists("estado.json"):
            with open("estado.json", "r") as estado_archivo:
                contenido = estado_archivo.read()

        estado = None
        if len(contenido) > 0:
            json = loads(contenido)
            estado = EstadoATM.create(json)

        return Estado(estado)


# Decorador para pasar el estado
pass_estado = click.make_pass_decorator(Estado)


class estado_atm(ContextDecorator):
    def __enter__(self):
        self.estado = Estado.cargar()
        return self.estado

    def __exit__(self, exc_type, exc, exc_tb):
        sys_exc = sys.exc_info()[1]
        if (
            isinstance(sys_exc, click.exceptions.Exit)
            and sys_exc.exit_code == 0
            and self.estado.rollback == False
        ):
            click.echo(f"Persistiendo estado del cajero...")
            self.estado.guardar()
