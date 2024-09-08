from json import dump, loads
from os.path import exists
import datetime


class Estado:
    """Modelo que representa el estado del sistema."""

    usuarios = {}
    dni_admin = 'admin'
    clave_admin = 'admin'
    saldo = 0
    movimientos = {}
    cant_max_usuarios = 5
    long_min_clave = 8

    def guardar(self):
        """Guarda la instancia actual del modelo de Estado en el archivo `estado.json`."""
        json = {}
        json["usuarios"] = self.usuarios
        json["saldo"] = self.saldo
        json["movimientos"] = self.movimientos
        with open("estado.json", "w") as estado_archivo:
            dump(json, estado_archivo, indent=4, sort_keys=True, default=str)
            # dump(json, estado_archivo)

    def movimientos_entre(self, dni_admin, clave_admin, dni_consulta, desde, hasta):

        if not self.autentificacion_admin(dni_admin, clave_admin):
            return {'resultado': None, 'info': 'Credenciales de Administrador Invalidas'}

        if not dni_consulta in self.movimientos.keys():
            return {'resultado': None, 'info': 'Dni no registrado'}

        movimientos_filtrados = []
        for movimiento in self.movimientos[dni_consulta]:
            fecha = datetime.datetime.strptime(
                movimiento[0], '%d/%m/%y %H:%M:%S')
            if fecha >= desde and fecha <= hasta:
                movimientos_filtrados.append(movimiento)

        return {'resultado': movimientos_filtrados, 'info': ''}

    def cargar():
        """Retorna una instancia del modelo de estado con los valores guardados en `estado.json`."""
        contenido = ""
        if exists("estado.json"):
            with open("estado.json", "r") as estado_archivo:
                contenido = estado_archivo.read()
        if contenido != "":
            json = loads(contenido)
            estado = Estado()
            estado.usuarios = json["usuarios"]
            estado.saldo = json["saldo"]
            estado.movimientos = json["movimientos"]
            return estado
        else:
            return Estado.__inicial()

    def autentificacion_admin(self, dni_admin, clave_admin):
        return dni_admin == self.dni_admin and clave_admin == self.clave_admin

    def existe_usuario_clave(self, dni, clave):
        if dni in self.usuarios.keys() and self.usuarios[dni]['clave'] == clave:
            return True
        return False

    def existe_usuario(self, dni):
        return (dni in self.usuarios.keys())

    def crear_usuario(self, dni, clave, sueldo):

        verificacion_clave = self.verificar_clave(clave)

        if not verificacion_clave['resultado']:
            return verificacion_clave

        if not self.existe_usuario(dni):
            self.usuarios[dni] = {
                'clave': clave, 'saldo': sueldo, 'movimientos': {}, 'sueldo': sueldo}
            self.movimientos[dni] = []
            return {'resultado': True, 'info': 'Usuario creado'}

        return {'resultado': False, 'info': 'Usuario ya existente'}

    def verificar_clave(self, clave):
        if not len(clave) >= self.long_min_clave:
            return {'resultado': False, 'info': 'Clave no cumple con la longitud mínima'}

        if not clave.isalnum():
            return {'resultado': False, 'info': 'La clave debe ser alfanumerica'}

        return {'resultado': True, 'info': 'Clave cumple con la validación'}

    def extraccion(self, dni, clave, monto):
        existe = self.existe_usuario_clave(dni, clave)
        if not existe:
            return {'resultado': False, 'info': 'No existe combinacion dni clave'}

        if not self.extraccion_restriccion_movimientos(dni):
            return {'resultado': False, 'info': 'No se puede por la restriccion.'}

        if self.saldo < monto:
            return {'resultado': False, 'info': 'Saldo de cajero insuficiente'}

        saldo = self.usuarios[dni]['saldo']

        if saldo >= monto:
            self.usuarios[dni]['saldo'] = saldo - monto
            self.saldo -= monto
            self.movimientos[dni].append(
                (datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), "Extraccion"))
            return {'resultado': True, 'info': 'Monto extraido'}
        else:
            return {'resultado': False, 'info': 'Saldo de usuario insuficiente'}

    def carga(self, dni_admin, clave_admin, monto):
        if not self.autentificacion_admin(dni_admin, clave_admin):
            return {'resultado': False, 'info': 'Credenciales de Administrador Invalidas'}

        self.saldo += monto

        return {'resultado': self.saldo, 'info': 'Monto cargado'}

    def alta(self, dni_admin, clave_admin,  dni, clave, sueldo):
        if not self.autentificacion_admin(dni_admin, clave_admin):
            return {'resultado': False, 'info': 'Credenciales de Administrador Invalidas'}

        if len(self.usuarios) == self.cant_max_usuarios:
            return {'resultado': False, 'info': 'Máxima cantidad de usuarios alcanzada.'}

        return self.crear_usuario(dni, clave, sueldo)

    def clave(self, dni, actual, nueva):
        existe = self.existe_usuario_clave(dni, actual)
        if not existe:
            return {'resultado': False, 'info': 'No existe combinacion dni clave'}

        if not self.clave_restriccion_movimientos(dni):
            return {'resultado': False, 'info': 'No se puede cambiar por la restriccion.'}

        verificacion_clave = self.verificar_clave(nueva)
        if verificacion_clave['resultado']:
            self.usuarios[dni]['clave'] = nueva
            self.movimientos[dni].append(
                (datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), "Clave"))
            return {'resultado': True, 'info': 'Clave cambiada'}
        else:
            return verificacion_clave

    def consulta_saldo(self, dni, clave):
        existe = self.existe_usuario_clave(dni, clave)
        if not existe:
            return {'resultado': False, 'info': 'No existe combinacion dni clave'}

        return {'resultado': self.usuarios[dni]['saldo'], 'info': 'Saldo: ' + str(self.usuarios[dni]['saldo'])}

    def __inicial():
        """Retorna una instancia del modelo de estado con sus valores iniciales."""
        estado = Estado()
        return estado

    def clave_restriccion_movimientos(self, dni_consulta):
        movimientos_filtrados = []

        ahora = datetime.datetime.now()
        inicio_mes = ahora
        inicio_mes = inicio_mes.replace(day=1)
        inicio_mes = inicio_mes.replace(second=0)
        inicio_mes = inicio_mes.replace(minute=0)
        inicio_mes = inicio_mes.replace(hour=0)

        for movimiento in self.movimientos[dni_consulta]:
            fecha = datetime.datetime.strptime(
                movimiento[0], '%d/%m/%y %H:%M:%S')
            if fecha >= inicio_mes and fecha <= ahora:
                movimientos_filtrados.append(movimiento)

        if len(movimientos_filtrados) > 0:
            return False
        return True

    def extraccion_restriccion_movimientos(self, dni_consulta):
        movimientos_filtrados = []

        ahora = datetime.datetime.now()
        inicio_dia = ahora
        inicio_dia = inicio_dia.replace(second=0)
        inicio_dia = inicio_dia.replace(minute=0)
        inicio_dia = inicio_dia.replace(hour=0)

        for movimiento in self.movimientos[dni_consulta]:
            fecha = datetime.datetime.strptime(
                movimiento[0], '%d/%m/%y %H:%M:%S')
            if fecha >= inicio_dia and fecha <= ahora:
                movimientos_filtrados.append(movimiento)

        if len(movimientos_filtrados) > 2:
            return False
        return True


Estado.cargar = staticmethod(Estado.cargar)
