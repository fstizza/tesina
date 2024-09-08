from soluciones import soluciones
from datetime import datetime


def promedio(datos: list[tuple[str, int]]) -> tuple[int, float]:
    filtrados = list(map(lambda e: e[1], filter(lambda d: d[1] > 0, datos)))
    return (sum(filtrados), sum(filtrados) / len(filtrados))


def formatear_float(numero: float) -> str:
    valor = f"{numero:.2f}"
    return valor.replace(".", ",")


def main() -> None:
    csv = "Nombre;Grupo;C. Ciclomática (TOT);C. Ciclomática (MED);C. Cognitiva (TOT);C. Cognitiva (MED);Líneas (TOT);Líneas (MED);Funciones (TOT);Funciones (MED);Archivos\n"
    for solucion in soluciones:
        nombre, grupo, ciclomatica, cognitiva, otros = solucion
        cantidad_lineas, cantidad_funciones, cantidad_archivos = otros

        ciclomatica_tot, ciclomatica_med = promedio(ciclomatica)
        cognitiva_tot, cognitiva_med = promedio(cognitiva)
        lineas_tot, lineas_med = promedio(cantidad_lineas)
        funciones_tot, funciones_med = promedio(cantidad_funciones)
        csv += f"{nombre};{grupo};{ciclomatica_tot};{formatear_float(ciclomatica_med)};{cognitiva_tot};{formatear_float(cognitiva_med)};{lineas_tot};{formatear_float(lineas_med)};{funciones_tot};{formatear_float(funciones_med)};{cantidad_archivos}\n"

    fecha = datetime.now().isoformat().replace(" ", "").replace(":", "_")

    with open(f"res_{fecha}.csv", "x") as archivo_resultado:
        archivo_resultado.write(csv)


if __name__ == "__main__":
    main()
