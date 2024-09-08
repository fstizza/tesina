from servicio import Servicio

class Operaciones:

    def extraccion(dni,clave,monto):
        if(Servicio.auth(dni,clave)):
            if(Servicio.extraccion(dni,monto)):
                print("Extraccion exitosa")
            else:
                print("No se ha podido realizar la extraccion")
        else:
            print("Error de credenciales")

    def clave(dni,actual,nueva):
        if (Servicio.auth(dni,actual)):
            if(Servicio.cambio_clave(dni,nueva)):
                print("Cambio de clave exitoso")
            else:
                print("No se ha podido cambiar la clave")
        else:
            print("Error de credenciales")
    def saldo(dni,clave):
        if(Servicio.auth(dni,clave)):
            Servicio.consultar_saldo(dni)
    def alta(dni_administrador, clave_administrador,dni,clave,nombre,sueldo):
        if(Servicio.auth_admin(dni_administrador,clave_administrador)):
            if(Servicio.alta(dni,clave,nombre,sueldo)):
                print("Alta de usuario exitosa")
            else:
                print("No se ha podido realizar el alta de usuario")
        else:
            print("Error de credenciales de administrador")
    def carga(dni_administrador,clave_administrador,monto):
        if(Servicio.auth_admin(dni_administrador,clave_administrador)):
            Servicio.carga(monto)
        else:
            print("Error de credenciales de administrador")

    def movimientos(dni_administrador,clave_administrador):
        if(Servicio.auth_admin(dni_administrador,clave_administrador)):
            Servicio.movimientos()
        else:
            print("Error de credenciales de administrador")
        
