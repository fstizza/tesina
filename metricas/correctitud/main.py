from argparse import ArgumentParser
from datetime import datetime
import os
from tests import obtener_pruebas
from soluciones import obtener_soluciones
from modelos import Solucion
import io
from contextlib import redirect_stdout


def ejecutar_pruebas(solucion: Solucion, pruebas: map, muestra_errores: bool) -> None:
    print(
        f"--> Ejecutando {len(pruebas)} pruebas sobre el experimento de {solucion.nombre}"
    )

    ok = []
    errores = []
    resultados = []
    for nombre, prueba in pruebas.items():
        print(nombre)
        res = prueba()
        if len(res) == 0:
            ok.append(nombre)
        else:
            errores.append((nombre, res))
        resultados.append(len(res) == 0)

    mensajes_errores = list(
        map(
            lambda x: "\t\t- {prueba}: {errores}\n".format(
                prueba=x[0], errores="\n\t\t\t\t & ".join(x[1])
            ),
            errores,
        )
    )

    print(f"\tOK: {len(ok)}")
    print(f"\tER: {len(errores)}")
    if muestra_errores and len(mensajes_errores) != 0:
        print("\n".join(mensajes_errores))

    return (
        solucion.nombre,
        len(pruebas),
        len(ok) / len(pruebas),
        errores,
        resultados,
    )


def main(filtro_soluciones: str, filtro_pruebas: str, muestra_errores: bool) -> None:
    soluciones = obtener_soluciones(filtro_soluciones)

    ahora = int(datetime.now().timestamp())
    if not os.path.exists(f"resultados/{ahora}"):
        os.mkdir(f"resultados/{ahora}")

    resultados = {}
    for solucion in soluciones:
        pruebas = obtener_pruebas(solucion, filtro_pruebas)
        nombre_normalizado = solucion.nombre.replace(" ", "_").lower()

        with open(f"resultados/{ahora}/{nombre_normalizado}.txt", "w") as f:
            with redirect_stdout(f):
                _, __, ____, _____, res = ejecutar_pruebas(
                    solucion, pruebas, muestra_errores
                )
                resultados[nombre_normalizado] = res

    csv = ""
    for participante, res in resultados.items():
        res = ", ".join(map(lambda e: "OK" if e else "ER", res))
        csv += f"{participante}, {res}\n"

    with open(f"resultados/{ahora}.csv", "w") as f:
        f.write(csv)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--solucion", "-s", required=False, type=str)
    parser.add_argument("--pruebas", "-p", required=False, type=str)
    parser.add_argument(
        "--errores", "-e", required=False, action="store_true", default=False
    )

    args = parser.parse_args()

    main(args.solucion, args.pruebas, args.errores)
