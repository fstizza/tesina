import datetime
from decimal import Context, Decimal, Inexact
import re
import click

TWOPLACES = Decimal(10) ** -2


class MoneyParamType(click.ParamType):
    name = "money"

    def convert(self, value, param, ctx):
        """Valida y convierte unidades de dinero.

        Las unidades de dinero pueden tener hasta dos decimales y deben ser positivas.
        """

        try:
            q = Decimal(value).quantize(TWOPLACES, context=Context(traps=[Inexact]))
            if q < 0:
                raise ValueError("monto negativo")
            return q
        except Inexact:
            self.fail(f"{value!r} tiene más de dos decimales", param, ctx)
        except (ValueError, ArithmeticError):
            self.fail(f"{value!r} no es un monto válido", param, ctx)


class DNIParamType(click.ParamType):
    name = "dni"

    def convert(self, value, param, ctx):
        """Valida y convierte DNI.

        Los DNI deben consistir de 7 u 8 dígitos, seguidos por opcionalmente una letra mayúscula.
        """

        if not re.fullmatch(r"\d{7,8}[A-Z]?", value):
            self.fail(f"{value!r} no es un DNI válido", param, ctx)

        return value


class ClaveParamType(click.ParamType):
    name = "clave"

    def convert(self, value, param, ctx):
        """Valida y convierte clave.

        Las claves deben poseer al menos 8 caracteres y ser una combinación de letras y números.
        """

        if not re.fullmatch(r"[a-zA-Z0-9]{8,}", value):
            self.fail(f"{value!r} no es una clave válida", param, ctx)

        return value


class FechaParamType(click.ParamType):
    name = "fecha"

    def convert(self, value, param, ctx):
        """Valida y convierte una fecha.

        Las fechas deben estar en formato YYYY-MM-DD.
        """

        try:
            d = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            self.fail(f"{value!r} no es una fecha válida", param, ctx)

        return d


MONEY = MoneyParamType()
DNI = DNIParamType()
CLAVE = ClaveParamType()
FECHA = FechaParamType()
