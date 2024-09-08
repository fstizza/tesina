class OperacionConsultaSaldo:
    def __init__(self,auth,repo_usuario):
        self.auth = auth
        self.repo_usuario = repo_usuario

    def correr(self,args):
        usuario = self.auth.autenticar_usuario(args["dni"], args["clave"])
        if usuario == None: 
            return "Clave invalida" 
        
        return usuario.cuenta.saldo
