from typing import Optional

from entidades.usuario import Usuario


class ServicioAutenticacion:
    def __init__(self, repo):
        self.repo = repo

    def autenticar_usuario(self,dni,clave) -> Optional[Usuario]:
        usuario = self.repo.buscarPorDNI(dni) 
        if usuario == None or usuario.clave != clave:
            return None

        return usuario

    def autenticar_admin(self,dni,clave) -> Optional[Usuario]:
        usuario = self.autenticar_usuario(dni,clave)
        if usuario == None or not usuario.es_admin():
            return None

        return usuario
