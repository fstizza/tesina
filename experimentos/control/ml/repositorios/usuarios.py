from estado import Estado
from entidades.usuario import Usuario 
from typing import Optional

class RepositorioUsuarios:
    def buscarPorDNI(self, dni) -> Optional[Usuario]:
        return self._buscarPorDNI(dni)    

    def agregar(self, usuario):
        e = Estado.cargar()
        e.usuarios.append(usuario)
        e.guardar()

    def actualizar(self, usuario_mod):
        usuario = self._buscarPorDNI(usuario_mod.dni)
        if usuario:
            usuario.clave = usuario_mod.clave
            usuario.nombre = usuario_mod.nombre
            usuario.dni = usuario_mod.dni
            usuario.sueldo = usuario_mod.sueldo
            usuario.cuenta = usuario_mod.cuenta
            
            self.estado.guardar()

    def movimientosPorRango(self, usuario, desde, hasta):
        return [ tx for tx in usuario.cuenta.movimientos if desde <= tx.fecha <= hasta ]

    def _buscarPorDNI(self, dni) -> Optional[Usuario]:
        self.estado = Estado().cargar() 
        for usuario in self.estado.usuarios:
            if usuario.dni == dni:
                return usuario
        return None

