from operacion import OperacionAdmin


class AltaUsuario(OperacionAdmin):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.dni = args[3]
        self.clave = args[4]
        self.nombre = args[5]
        self.sueldo = int(args[6])
        self.saldo = int(args[7])

    def execute(self):
        if self.auth_admin() == False:
            raise Exception("Auth admin")

        if self.valid() == False:
            raise Exception("Alta de usuario no permitido")

        new_user = {"dni": self.dni, "nombre": self.nombre, "sueldo": self.sueldo}
        self.e.user_list.append(new_user)
        new_account = {"dni": self.dni, "clave": self.clave, "saldo": self.saldo}
        self.e.account_list.append(new_account)

    def valid(self):
        return (
            self.valid_new_user()
            and self.valid_user_amount()
            and self.valid_system_capacity()
        )

    def valid_new_user(self):
        user_list = self.e.user_list
        user = next((item for item in user_list if item["dni"] == self.dni), None)
        return user == None

    def valid_system_capacity(self):
        return len(self.e.user_list) < 5

    def valid_user_amount(self):
        return self.sueldo == self.saldo
