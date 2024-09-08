from os import sys
from args import ArgSanitizador
from operaciones.actualizar_clave import OperactionActualizarClave
from operaciones.carga_cajero import OperacionCargaCajero
from operaciones.consulta_saldo import OperacionConsultaSaldo
from operaciones.extraccion import OperacionExtraccion
from operaciones.alta_usuario import OperacionAltaUsuario
from operaciones.busqueda_movimientos import OperacionBusquedaMovimientos 
from repositorios.cajeros import RepositorioCajero
from repositorios.usuarios import RepositorioUsuarios
from servicios.autenticacion import ServicioAutenticacion 
from datetime import datetime


def main(args: list):
    if len(args) == 0:
        print("Sin argumentos.")
        exit(1)


    sanitizer = ArgSanitizador(args[1:])

    repo_usuario = RepositorioUsuarios()
    repo_cajero = RepositorioCajero()

    auth = ServicioAutenticacion(repo_usuario) 

    if args[0] == "extraccion":
        param_requirements = [
        ("dni", int, lambda x: x > 0),
        ("clave", str, lambda x: x.isalnum()),
        ("monto", int, lambda _: True),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperacionExtraccion(auth,repo_cajero,repo_usuario)

        out = s.correr(args)
        print(out)
    elif args[0] == "clave":
        param_requirements = [
        ("dni", int, lambda x: x > 0),
        ("actual", str, lambda x: x.isalnum()),
        ("nueva", str, lambda x: x.isalnum()),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperactionActualizarClave(auth,repo_usuario)

        out = s.correr(args)
        print(out)

        # TODO: Completar.
        pass
    elif args[0] == "saldo":
        param_requirements = [
        ("dni", int, lambda x: x > 0),
        ("clave", str, lambda x: x.isalnum()),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperacionConsultaSaldo(auth,repo_usuario)

        out = s.correr(args)
        print(out)
    elif args[0] == "alta":
        param_requirements = [
        ("dni_administrador", int, lambda x: x > 0),
        ("clave_administrador", str, lambda x: x.isalnum()),
        ("dni", int, lambda x: x > 0),
        ("clave", str, lambda x: x.isalnum()),
        ("nombre", str, lambda x: x.isalnum()),
        ("sueldo", int, lambda x: x > 0),
        ("saldo", int, lambda x: x > 0),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperacionAltaUsuario(auth,repo_usuario)

        out = s.correr(args)
        print(out)
    elif args[0] == "carga":
        param_requirements = [
        ("dni_administrador", int, lambda x: x > 0),
        ("clave_administrador", str, lambda x: x.isalnum()),
        ("monto", int, lambda x: x > 0),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperacionCargaCajero(auth,repo_cajero)

        out = s.correr(args)
        print(out)
    elif args[0] == "movimientos":
        param_requirements = [
        ("dni_administrador", int, lambda x: x > 0),
        ("clave_administrador", str, lambda x: x.isalnum()),
        ("dni_consulta", int, lambda x: x > 0),
        ("desde", str, lambda x: datetime.strptime(x, '%Y-%m-%d')),
        ("hasta", str, lambda x: datetime.strptime(x, '%Y-%m-%d')),
        ]

        args = sanitizer.sanitizar(param_requirements)

        s = OperacionBusquedaMovimientos(auth,repo_usuario)

        out = s.correr(args)
        print(out)
    else:
        print("Operación inválida.")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
