import re 
class OperactionActualizarClave:
    def __init__(self,auth,repo_usuario):
        self.auth = auth
        self.repo_usuario = repo_usuario 

    def correr(self,args):
        usuario = self.auth.autenticar_usuario(args["dni"], args["actual"])
        if usuario == None: 
            return "Clave invalida" 

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', args["nueva"]):
            return "Clave debil"

        resultado = usuario.cambiar_clave(args["nueva"])
        if resultado != None:
            return resultado

        self.repo_usuario.actualizar(usuario) 

        return "Exito!"
