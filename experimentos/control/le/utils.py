import click


def echo_ok(msg):
    """Imprime mensaje de éxito"""
    click.echo(click.style(msg, fg="green"))


def echo_err(msg):
    """Imprime mensaje de error"""
    click.echo(click.style(msg, fg="red", bold=True))
