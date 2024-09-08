from estado import Estado

class Servicio:
    
    def auth(dni,clave):
        e = Estado.cargar()
        for usuario in e.usuarios:
            if usuario["dni"] == dni and usuario["clave"] == clave:
                return True
        return False
    
    def auth_admin(dni,clave):
        e = Estado.cargar()
        for admin in e.admins:
            if admin["dni"] == dni and admin["clave"] == clave:
                return True
        return False
    
    def extraccion(dni,monto):
        e = Estado.cargar()
        if e.disponible >= monto:
            for cuenta in e.cuentas:
                if cuenta["dni"] == dni:
                    if cuenta["saldo"] >= monto:
                        cuenta["saldo"] = cuenta["saldo"] - monto
                        print("Saldo actual: ",cuenta["saldo"])
                        nuevo_log = {"dni":dni,"tipo":"Extraccion","valor":monto}
                        e.logs.append(nuevo_log)
                        e.disponible = e.disponible - monto
                        e.guardar()
                        return True
        return False
    
    def cambio_clave(dni,nueva_clave):
        e = Estado.cargar()
        for usuario in e.usuarios:
            if usuario["dni"] == dni:
                usuario["clave"] = nueva_clave
                nuevo_log = {"dni":dni,"tipo":"Cambio clave","valor":nueva_clave}
                e.logs.append(nuevo_log)
                e.guardar()
                return True
        return False
    
    def consultar_saldo(dni):
        e = Estado.cargar()
        for cuenta in e.cuentas:
            if(cuenta["dni"] == dni):
                return print("Saldo actual: ",cuenta["saldo"])
        return print("No existe cuenta asociada al usuario")
    
    def alta(dni,clave,nombre,sueldo):
        e = Estado.cargar()
        if e.totalusers <= 5:
            nuevo_user = {"dni":dni,"clave":clave,"nombre":nombre,"sueldo_mensual":sueldo}
            nueva_cuenta = {"dni":dni,"saldo":sueldo}
            e.usuarios.append(nuevo_user)
            e.cuentas.append(nueva_cuenta)
            e.totalusers = e.totalusers + 1
            e.guardar()
            return True
        else:
            return False
    
    def carga(monto):
        e = Estado.cargar()
        e.disponible = e.disponible + monto
        print("Saldo actual del cajero: ",e.disponible)
        e.guardar()

    def movimientos():
        e = Estado.cargar()
        print("Movimientos del cajero:")
        print("_______________________")
        print("")
        for log in e.logs:
            print("Usuario: ",log["dni"]," ",log["tipo"]," ",log["valor"])