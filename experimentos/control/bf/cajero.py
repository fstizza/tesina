from estado import Estado
from datetime import datetime as dt

class Cajero:

    def __init__(self) -> None:
        self.__estado = Estado.cargar()
        

    def extraccion(self, dni, clave, monto):
        if(dni not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni}')
            return
        
        caja = self.__estado.usuarios[dni]

        if clave != caja['clave']:
            print(f'ERROR: Usuario y/o clave incorrecto')
            return
        
        if monto > caja['sueldo']/2:
            print(f'ERROR: monto demasiado alto')
            return
        
        if monto > self.__estado.saldo:
            print(f'ERROR: dinero insuficiente en el cajero')
            return

        time = dt.now()
        extraciones_hoy = [d for d, m in caja['movimientos'].items() if m['op'] == 'extraccion' and dt.fromisoformat(d).date() == time.date()]
        if len(extraciones_hoy) >= 3:
            print(f'ERROR: limite de extracciones diarias alcanzado')
            return
        
        caja['saldo'] -= monto
        caja['movimientos'][time.isoformat()] = {'op': 'extraccion', 'monto': monto}
        self.__estado.guardar()


    def cambio_clave(self, dni, actual, nueva: str):
        if(dni not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni}')
            return
        
        caja = self.__estado.usuarios[dni]

        if actual != caja['clave']:
            print(f'ERROR: Usuario y/o clave incorrecto')
            return

        time = dt.now()
        cambios_mes = [d for d, m in caja['movimientos'].items() if m['op'] == 'cambio_clave' and dt.fromisoformat(d).month == time.month]
        if cambios_mes:
            print(f'ERROR: limite de cambios de claves mensuales alcanzado')
            return
        
        if len(nueva) < 8:
            print(f'ERROR: la clave nueva es demasiado corta, por favor use al menos 8 caracteres')
            return
        
        if nueva.isalnum() and any(c.isalpha() for c in nueva) and any(c.isdecimal() for c in nueva):
            caja['clave'] = nueva
            caja['movimientos'][time.isoformat()] = {
                'op': 'cambio_clave',
                'clave_anterior': actual,
                'clave_nueva': nueva
            }
            self.__estado.guardar()
            return
        
        print(f'ERROR: la clave nueva debe ser una convinacion de letras y numeros')

    def consulta_saldo(self, dni, clave):
        if(dni not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni}')
            return
        
        caja = self.__estado.usuarios[dni]

        if clave != caja['clave']:
            print(f'ERROR: Usuario y/o clave incorrecto')
            return
        
        return caja['saldo']
        

    def alta_usuario(self, dni_admin, clave_admin, dni, clave, nombre, sueldo, saldo):
        if(dni_admin not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni_admin}')
            return
        
        caja_admin = self.__estado.usuarios[dni_admin]

        if clave_admin != caja_admin['clave']:
            print(f'ERROR: Usuario y/o clave incorrecto')
            return
        
        if not caja_admin['admin']:
            print('ERROR: Esta operacion esta disponible solo para usuarios administradores')
            return
        
        if dni in self.__estado.usuarios.keys():
            print(f'ERROR: El dni {dni} ya posee una caja')
            return
    
        if len(self.__estado.usuarios) >= 5:
            print(f'ERROR: El cajero alcanzo el numero maximo de usuarios')
            return
        
        if sueldo != saldo:
            print(f'ERROR: El saldo no coincide con el sueldo mensual')
            return
        
        nuevo_usuario = {
            "nombre": nombre,
            "sueldo": sueldo,
            "clave": clave,
            "saldo": saldo,
            "movimientos": {},
            "admin": False
        }

        self.__estado.usuarios[dni] = nuevo_usuario
        self.__estado.guardar()

        

    def carga_cajero(self, dni_admin, clave_admin, monto):
        if(dni_admin not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni_admin}')
            return
        
        caja_admin = self.__estado.usuarios[dni_admin]

        if clave_admin != caja_admin['clave']:
            print(f'ERROR: dni y/o clave incorrecto')
            return
        
        if not caja_admin['admin']:
            print('ERROR: Esta operacion esta disponible solo para usuarios administradores')
            return
        
        self.__estado.saldo += monto
        self.__estado.guardar()


    def consulta_movimientos(self, dni_admin, clave_admin, dni, desde, hasta):
        if(dni_admin not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni_admin}')
            return
        
        caja_admin = self.__estado.usuarios[dni_admin]

        if clave_admin != caja_admin['clave']:
            print(f'ERROR: Usuario y/o clave incorrecto')
            return
        
        if not caja_admin['admin']:
            print('ERROR: Esta operacion esta disponible solo para usuarios administradores')
            return
        
        if(dni not in self.__estado.usuarios.keys()):
            print(f'ERROR: No existe el usuario con dni {dni}')
            return
        
        caja = self.__estado.usuarios[dni]

        movimientos_deseados = [{fecha: mov} for fecha, mov in caja['movimientos'].items() if dt.fromisoformat(fecha) >= desde and dt.fromisoformat(fecha) <= hasta]
        return movimientos_deseados
