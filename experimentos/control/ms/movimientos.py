from operacion import OperacionAdmin
from datetime import datetime


class Movimientos(OperacionAdmin):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.dni_consulta = args[3]
        self.desde = datetime.strptime(args[4], self.datetime_format())
        self.hasta = datetime.strptime(args[5], self.datetime_format())

    def execute(self):
        if self.auth_admin() == False:
            raise Exception("Extraccion no permitida")

        if self.valid() == False:
            raise Exception("Consulta de movimientos no permitida")

        movements = [
            entry
            for entry in self.e.mov_list
            if self.desde
            <= datetime.strptime(entry["date"], self.datetime_format())
            <= self.hasta
        ]

        for entry in movements:
            print(entry)

    def valid(self):
        return self.valid_user()

    def valid_user(self):
        user_list = self.e.user_list
        user = next(
            (item for item in user_list if item["dni"] == self.dni_consulta), None
        )
        return user != None
