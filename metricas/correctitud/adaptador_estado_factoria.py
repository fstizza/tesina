from metricas.correctitud.adaptadores.at import AdaptadorAT
from metricas.correctitud.adaptadores.at2 import AdaptadorAT2
from metricas.correctitud.adaptadores.bm import AdaptadorBM
from metricas.correctitud.adaptadores.bv import AdaptadorBV
from metricas.correctitud.adaptadores.cd import AdaptadorCD
from metricas.correctitud.adaptadores.dp import AdaptadorDP
from metricas.correctitud.adaptadores.df import AdaptadorDF
from metricas.correctitud.adaptadores.dl import AdaptadorDL
from metricas.correctitud.adaptadores.fe import AdaptadorFE
from metricas.correctitud.adaptadores.fl import AdaptadorFL
from metricas.correctitud.adaptadores.gt import AdaptadorGT
from metricas.correctitud.adaptadores.gf import AdaptadorGF
from metricas.correctitud.adaptadores.ij import AdaptadorIJ
from metricas.correctitud.adaptadores.le import AdaptadorLE
from metricas.correctitud.adaptadores.mj import AdaptadorMJ
from metricas.correctitud.adaptadores.ml import AdaptadorML
from metricas.correctitud.adaptadores.ms import AdaptadorMS
from metricas.correctitud.adaptadores.nn import AdaptadorNN
from metricas.correctitud.adaptadores.nm import AdaptadorNM
from metricas.correctitud.adaptadores.nd import AdaptadorND
from metricas.correctitud.adaptadores.pg import AdaptadorPG
from metricas.correctitud.adaptadores.pm import AdaptadorPM
from metricas.correctitud.adaptadores.sa import AdaptadorSA
from metricas.correctitud.adaptadores.vl import AdaptadorVL
from metricas.correctitud.adaptadores.wg import AdaptadorWG
from metricas.correctitud.adaptadores.ws import AdaptadorWS
from metricas.correctitud.adaptadores.bf import AdaptadorBF
from metricas.correctitud.adaptadores.bm2 import AdaptadorBM2


class AdaptadorEstadoFactoria:
    def __init__(self) -> None:
        pass

    def obtenerAdaptador(adaptador: str):
        if adaptador == "at":
            return AdaptadorAT()
        if adaptador == "at2":
            return AdaptadorAT2()
        if adaptador == "bm":
            return AdaptadorBM()
        if adaptador == "bm2":
            return AdaptadorBM2()
        if adaptador == "bv":
            return AdaptadorBV()
        if adaptador == "bf":
            return AdaptadorBF()
        if adaptador == "cd":
            return AdaptadorCD()
        if adaptador == "dp":
            return AdaptadorDP()
        if adaptador == "df":
            return AdaptadorDF()
        if adaptador == "dl":
            return AdaptadorDL()
        if adaptador == "fe":
            return AdaptadorFE()
        if adaptador == "fl":
            return AdaptadorFL()
        if adaptador == "gt":
            return AdaptadorGT()
        if adaptador == "gf":
            return AdaptadorGF()
        if adaptador == "ij":
            return AdaptadorIJ()
        if adaptador == "le":
            return AdaptadorLE()
        if adaptador == "mj":
            return AdaptadorMJ()
        if adaptador == "ml":
            return AdaptadorML()
        if adaptador == "ms":
            return AdaptadorMS()
        if adaptador == "nn":
            return AdaptadorNN()
        if adaptador == "nm":
            return AdaptadorNM()
        if adaptador == "nd":
            return AdaptadorND()
        if adaptador == "pg":
            return AdaptadorPG()
        if adaptador == "pm":
            return AdaptadorPM()
        if adaptador == "sa":
            return AdaptadorSA()
        if adaptador == "vl":
            return AdaptadorVL()
        if adaptador == "wg":
            return AdaptadorWG()
        if adaptador == "ws":
            return AdaptadorWS()


AdaptadorEstadoFactoria.obtenerAdaptador = staticmethod(
    AdaptadorEstadoFactoria.obtenerAdaptador
)
