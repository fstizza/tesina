from datetime import datetime
from subprocess import CompletedProcess


def fechas_iguales(f1: datetime, f2: datetime) -> bool:
    return f1.day == f2.day and f1.month == f2.month and f1.year == f2.year


class Solucion:
    nombre: str
    lenguaje: str
    adaptador: str
    directorio: str
    no_usa_fecha: bool
    no_usa_sueldo: bool
    no_usa_tipo_operacion: bool
    dni_administrador: str
    clave_administrador: str
    nombre_proyecto_net: str
    require_argumento_saldo: bool

    def __init__(
        self,
        nombre: str,
        lenguaje: str,
        adaptador: str,
        directorio: str,
        no_usa_fecha: bool = False,
        no_usa_sueldo: bool = False,
        no_usa_tipo_operacion: bool = False,
        dni_administrador: str = "",
        clave_administrador: str = "",
        nombre_proyecto_net: str = "Solucion.csproj",
        require_argumento_saldo: bool = False,
    ) -> None:
        self.nombre = nombre
        self.lenguaje = lenguaje
        self.adaptador = adaptador
        self.directorio = directorio
        self.no_usa_fecha = no_usa_fecha
        self.no_usa_sueldo = no_usa_sueldo
        self.no_usa_tipo_operacion = no_usa_tipo_operacion
        self.dni_administrador = dni_administrador
        self.clave_administrador = clave_administrador
        self.nombre_proyecto_net = nombre_proyecto_net
        self.require_argumento_saldo = require_argumento_saldo


class Usuario:
    dni: str
    clave: str
    nombre: str
    sueldo: int
    saldo: int

    def __init__(
        self, dni: str, clave: str, nombre: str, sueldo: int, saldo: int
    ) -> None:
        self.dni = dni
        self.clave = clave
        self.nombre = nombre
        self.sueldo = sueldo
        self.saldo = saldo

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Usuario):
            return (
                self.dni == __value.dni
                and self.clave == __value.clave
                and self.saldo == __value.saldo
                and self.sueldo == __value.sueldo
            )
        return False

    def __lt__(self, other):
        return self.dni < other.dni

    def __str__(self) -> str:
        return f"U-(DNI: {self.dni}, Clave: {self.clave}, Nombre: {self.nombre}, Saldo: {self.saldo} Sueldo: {self.sueldo})"


class Movimiento:
    dni: str
    operacion: int
    fecha: datetime

    def __init__(self, dni: str, operacion: str, fecha: datetime, valor=None) -> None:
        self.dni = dni
        self.operacion = operacion
        self.fecha = fecha
        self.valor = valor

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Movimiento):
            return (
                self.dni == __value.dni
                and self.operacion == __value.operacion
                and fechas_iguales(self.fecha, __value.fecha)
            )
        return False

    def __lt__(self, other):
        if str(self.dni) == str(other.dni):
            if self.fecha == other.fecha:
                return self.operacion < other.operacion
            return self.fecha < other.fecha
        return str(self.dni) < str(other.dni)

    def __str__(self) -> str:
        return f"M-(DNI: {self.dni}, OP: {self.operacion}, Fecha: {self.fecha.isoformat()})"


class Estado:
    saldo: int
    usuarios: list[Usuario]
    movimientos: list[Movimiento]
    dni_administrador: str
    clave_administrador: str

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Estado):
            return (
                self.saldo == __value.saldo
                and sorted(self.usuarios) == sorted(__value.usuarios)
                and sorted(self.movimientos) == sorted(__value.movimientos)
            )
        return False

    def __str__(self) -> str:
        return f"-> Saldo: {self.saldo}\n-> Usuarios: {list(map(str, self.usuarios))}\n-> Movimientos: {list(map(str, self.movimientos))}"

    def toJson(self) -> map:
        movimientos = list(
            map(
                lambda m: {
                    "dni": m.dni,
                    "operacion": m.operacion,
                    "fecha": m.fecha.isoformat(),
                    "valor": m.valor,
                },
                self.movimientos,
            )
        )

        usuarios = list(
            map(
                lambda u: {
                    "dni": u.dni,
                    "clave": u.clave,
                    "nombre": u.nombre,
                    "sueldo": u.sueldo,
                    "saldo": u.saldo,
                },
                self.usuarios,
            )
        )

        return {
            "saldo": self.saldo,
            "movimientos": movimientos,
            "usuarios": usuarios,
        }


class ResultadoOperacion:
    inicial: Estado
    final: Estado
    salida: str
    salida_error: str
    codigo: int

    def __init__(
        self,
        inicial: Estado,
        resultado: CompletedProcess,
        final: Estado,
    ) -> None:
        self.inicial = inicial
        self.salida = resultado.stdout.decode("latin-1")
        self.salida_error = resultado.stderr.decode("latin-1")
        self.codigo = resultado.returncode
        self.final = final

    def transiciono(self) -> bool:
        return self.final != self.inicial

    def delta(self) -> list[str]:
        deltas = []
        if self.inicial.saldo != self.final.saldo:
            deltas.append(
                f"El saldo difiere. I ({self.inicial.saldo}) - F ({self.final.saldo})"
            )

        if sorted(self.inicial.usuarios) != sorted(self.final.usuarios):
            deltas.append(
                f"Usuarios:\nI ({list(map(str,self.inicial.usuarios))})\nF ({list(map(str,self.final.usuarios))})"
            )

        if sorted(self.inicial.movimientos) != sorted(self.final.movimientos):
            deltas.append(
                f"Movimientos:\nI ({list(map(str,self.inicial.movimientos))})\nF ({list(map(str,self.final.movimientos))})"
            )

        return deltas
