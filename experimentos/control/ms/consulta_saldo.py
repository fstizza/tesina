from operacion import OperacionUser


class ConsultaSaldo(OperacionUser):
    def __init__(self, e, args):
        super().__init__(e, args)

    def execute(self):
        super().execute()
        print(self.account["saldo"])
        return
