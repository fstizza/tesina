class OperacionCargaCajero:
    def __init__(self,auth,repo_cajero):
        self.auth = auth
        self.repo_cajero = repo_cajero

    def correr(self,args):
        if self.auth.autenticar_admin(args["dni_administrador"], args["clave_administrador"]) == None:
            return "credenciales de admin invalidas"
        
        cajero = self.repo_cajero.cajero()

        cajero.cargar(args["monto"])

        self.repo_cajero.actualizar(cajero)

        return "Exito!"
