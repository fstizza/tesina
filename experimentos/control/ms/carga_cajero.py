from operacion import OperacionAdmin


class CargaCajero(OperacionAdmin):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.monto = int(args[3])

    def execute(self):
        if self.auth_admin() == False:
            raise Exception("Auth admin")

        if self.valid() == False:
            raise Exception("Carga de cajero no permitida")

        self.e.saldo_cajero += self.monto

    def valid(self):
        return self.monto > 0
