from entidades.usuario import Usuario,Cuenta

class OperacionAltaUsuario:
    def __init__(self,auth, repo) -> None:
        self.auth = auth 
        self.repo = repo

    def correr(self,args):
        if self.auth.autenticar_admin(args["dni_administrador"], args["clave_administrador"]) == None:
            return "credenciales de admin invalidas"

        usuario = self.repo.buscarPorDNI(args["dni"])
        if usuario != None:
            return "usuario ya existente"
       
        cuenta = Cuenta(args["sueldo"],[])
        usuario = Usuario(
            args["dni"],
            args["clave"],
            args["nombre"],
            args["sueldo"],
            False,
            cuenta
        )

        self.repo.agregar(usuario)

        return "Exito!"
