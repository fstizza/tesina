import os
from adaptador_estado_factoria import AdaptadorEstadoFactoria
from modelos import ResultadoOperacion, Solucion, Estado
from subprocess import CompletedProcess, run
from os import chdir, curdir
from os.path import dirname, join
from json import dumps


def ejecutar_operacion(
    solucion: Solucion,
    inicial: Estado,
    operacion: str,
    *wargs,
) -> ResultadoOperacion:
    directorio_actual: str = os.getcwd()

    ruta = join(dirname(__file__), "../../experimentos", solucion.directorio)

    chdir(ruta)

    adaptador: AdaptadorEstadoFactoria = AdaptadorEstadoFactoria.obtenerAdaptador(
        solucion.adaptador
    )

    adaptador.guardar(inicial)

    comando: str = ""

    if solucion.lenguaje == "C#":
        comando = f"dotnet run --project {solucion.nombre_proyecto_net}"
    elif solucion.lenguaje == "Python":
        comando = "py main.py"
    elif solucion.lenguaje == "JavaScript":
        comando = "node index.js"
    else:
        raise Exception("ERROR")

    comando += f" {operacion} " + " ".join(wargs)

    resultado: CompletedProcess = run(comando, shell=True, capture_output=True)

    final: Estado = adaptador.cargar()

    chdir(directorio_actual)

    res = ResultadoOperacion(inicial, resultado, final)

    if True:
        print("--> STDOUT:\n", res.salida)
        print("--> STDERR:\n", res.salida_error)
        print("--> EXIT_CODE:\n", res.codigo)
        print("--> INICIAL:\n", dumps(res.inicial.toJson()))
        print("--> FINAL:\n", dumps(res.final.toJson()))

    return res
