from operaciones.autorizadores.exito import LimiteExito
from operaciones.autorizadores.limite_diario import LimiteDiario 
from operaciones.autorizadores.limit_monto import LimiteMonto


class OperacionExtraccion:
    def __init__(self,auth,repo_cajero,repo_usuario):
        self.auth = auth
        self.repo_cajero = repo_cajero
        self.repo_usuario = repo_usuario 


    def correr(self,args):
        monto = args["monto"]
        usuario = self.auth.autenticar_usuario(args["dni"], args["clave"])
        if usuario == None: 
            return "Clave invalida" 
        
        auth = self._autorizador()
        resultado = auth.autorizar(usuario,monto)
        if resultado != None:
            return resultado

        cajero = self.repo_cajero.cajero()

        resultado = usuario.cuenta.debito(monto)
        if resultado != None:
            return resultado

        resultado = cajero.extraer(monto)
        if resultado != None:
            return resultado

        self.repo_usuario.actualizar(usuario)
        self.repo_cajero.actualizar(cajero)

        return "Exito!"

    def _autorizador(self):
        return LimiteMonto(self.repo_usuario,LimiteDiario(self.repo_usuario, LimiteExito()))
