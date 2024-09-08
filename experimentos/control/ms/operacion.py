from auth import AuthAdmin, AuthUser


class Operacion:
    def __init__(self, e, args):
        self.e = e

    def valid(self):
        pass

    def datetime_format(self):
        return "%m/%d/%Y, %H:%M:%S"


class OperacionUser(Operacion):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.dni = args[1]
        self.clave = args[2]

    def execute(self):
        self.auth_user()
        if self.user == None:
            raise Exception("No encontro al usuario")
            return
        if self.account == None:
            raise Exception("No encontro la cuenta")
            return

    def auth_user(self):
        auth = AuthUser()
        self.user, self.account = auth.execute(self.e, self.dni, self.clave)


class OperacionAdmin(Operacion):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.dni_admin = args[1]
        self.clave_admin = args[2]

    def auth_admin(self):
        auth = AuthAdmin()
        return auth.execute(self.e, self.dni_admin, self.clave_admin)
