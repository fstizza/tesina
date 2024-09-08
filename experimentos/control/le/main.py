import datetime
from decimal import Decimal
import click

from estado import Estado, estado_atm, pass_estado
import utils
from datatypes import CLAVE, FECHA, MONEY, DNI


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = ctx.with_resource(estado_atm())


@cli.command("extraccion", help="Extracción")
@click.argument("dni", type=DNI)
@click.argument("clave", type=str)
@click.argument("monto", type=MONEY)
@pass_estado
def cmd_extraccion(estado: Estado, dni, clave, monto: Decimal):
    """Extrae MONTO de la cuenta DNI con CLAVE"""

    if not estado.login(dni, clave):
        utils.echo_err("Acceso denegado")
        return

    if monto > estado.saldo:
        utils.echo_err(
            f"Este cajero no tiene suficiente efectivo como para retirar {monto}"
        )
        return

    if monto * 2 > estado.obtener_sueldo(dni):
        utils.echo_err(f"Usted no puede realizar una extracción tan grande")
        return

    retiro = estado.retirar_dinero(dni, monto)
    if retiro == "OK":
        utils.echo_ok(f"Retirados {monto} de la cuenta {dni}")
    else:
        utils.echo_err(f"No se pudo completar el retiro solicitado: {retiro}")


@cli.command("clave", short_help="Cambio de Clave")
@click.argument("dni", type=DNI)
@click.argument("actual", type=str)
@click.argument("nueva", type=CLAVE)
@pass_estado
def cmd_clave(estado: Estado, dni, actual, nueva):
    """Cambia la clave de la cuenta DNI de ACTUAL a NUEVA"""
    if not estado.login(dni, actual):
        utils.echo_err("Acceso denegado")
        return

    if not estado.cambiar_clave(dni, nueva):
        utils.echo_err("No puede cambiar su clave tan seguido")
        return

    utils.echo_ok(f"La clave de la cuenta {dni} ha sido cambiada")


@cli.command("saldo", short_help="Consulta de Saldo")
@click.argument("dni", type=DNI)
@click.argument("clave", type=str)
@pass_estado
def cmd_saldo(estado, dni, clave):
    """Verifica saldo de la cuenta DNI con CLAVE"""
    if not estado.login(dni, clave):
        utils.echo_err("Acceso denegado")
        return

    saldo = estado.obtener_saldo(dni)
    utils.echo_ok(f"El saldo actual de la cuenta {dni} es de {saldo}")


@cli.command("alta", short_help="Alta de usuario")
@click.argument("dni_admin", type=DNI)
@click.argument("clave_admin", type=str)
@click.argument("dni", type=DNI)
@click.argument("clave", type=str)
@click.argument("nombre", type=str)
@click.argument("sueldo", type=int)
@pass_estado
def cmd_alta(estado: Estado, dni_admin, clave_admin, dni, clave, nombre, sueldo):
    """Siendo DNI_ADMIN con CLAVE_ADMIN, crea nueva cuenta con DNI, CLAVE, NOMBRE, SUELDO y SALDO"""

    if not estado.login(dni_admin, clave_admin, admin=True):
        utils.echo_err("Acceso admin denegado")
        return

    if (error := estado.alta(dni, clave, nombre, sueldo)) != "OK":
        utils.echo_err(f"Error creando cuenta: {error}")
        return

    utils.echo_ok(f"Cuenta para el usuario {dni} creada")


@cli.command("carga", short_help="Carga de Cajero")
@click.argument("dni_admin", type=DNI)
@click.argument("clave_admin", type=str)
@click.argument("monto", type=MONEY)
@pass_estado
def cmd_carga(estado, dni_admin, clave_admin, monto: Decimal):
    """Siendo DNI_ADMIN con CLAVE_ADMIN, carga el cajero con MONTO"""

    if not estado.login(dni_admin, clave_admin, admin=True):
        utils.echo_err("Acceso admin denegado")
        return

    estado.saldo += monto
    utils.echo_ok(f"Cajero cargado con {monto}. Saldo actual: {estado.saldo}")


@cli.command("movimientos", short_help="Consulta de movimientos")
@click.argument("dni_admin", type=DNI)
@click.argument("clave_admin", type=str)
@click.argument("dni", type=DNI)
@click.argument("desde", type=FECHA)
@click.argument("hasta", type=FECHA)
@pass_estado
def cmd_movimientos(estado, dni_admin, clave_admin, dni, desde, hasta):
    """Siendo DNI_ADMIN con CLAVE_ADMIN, consulta los movimientos de la cuenta DNI en las fechas DESDE a HASTA, ambas inclusive"""

    if not estado.login(dni_admin, clave_admin, admin=True):
        utils.echo_err("Acceso admin denegado")
        return

    if desde > hasta:
        utils.echo_err("Fecha desde posterior a hasta")
        return

    delta_dias = (hasta - desde).days + 1
    for delta in range(delta_dias):
        dia = desde + datetime.timedelta(days=delta)
        movimientos = estado.consultar_movimientos(dni, dia)
        utils.echo_ok(f"Movimientos del {dia}:")
        if len(movimientos) == 0:
            click.echo("Nada que reportar")
            continue

        for m in movimientos:
            click.echo(
                f"* {m.tipo}{f' de {m.monto}' if m.tipo == 'Extracción' else ''}"
            )


if __name__ == "__main__":
    cli()
