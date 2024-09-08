from datetime import datetime

class OperacionBusquedaMovimientos:
    def __init__(self,auth,user_repo) -> None:
        self.auth = auth
        self.user_repo = user_repo

    def correr(self,args):
        if self.auth.autenticar_admin(args["dni_administrador"], args["clave_administrador"]) == None:
            return "credenciales de admin invalidas"
        
        usuario = self.user_repo.buscarPorDNI(args["dni_consulta"])
        if usuario == None:
            return "usuario no existe"

        desde = datetime.strptime(args["desde"], '%Y-%m-%d')
        hasta = datetime.strptime(args["hasta"], '%Y-%m-%d')

        movimientos = self.user_repo.movimientosPorRango(usuario, desde,hasta)
        return [m.to_dict() for m in movimientos]


