from operacion import OperacionUser
from datetime import datetime, timedelta


class Extraccion(OperacionUser):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.monto = int(args[3])

    def execute(self):
        super().execute()
        if self.valid() == False:
            raise Exception("Extraccion no permitida")

        self.account["saldo"] -= self.monto
        self.e.saldo_cajero -= self.monto
        self.e.mov_list.append(
            {
                "mov_type": "extraccion",
                "dni": self.dni,
                "monto": self.monto,
                "date": datetime.now().strftime(self.datetime_format()),
            }
        )
        return

    def valid(self):
        return self.valid_extraction_attempt() and self.valid_amount()

    def valid_extraction_attempt(self):
        current_time = datetime.now()
        time_24_hours_ago = current_time - timedelta(hours=24)

        movements = [
            entry
            for entry in self.e.mov_list
            if entry["mov_type"] == "extraccion"
            and entry["dni"] == self.dni
            and datetime.strptime(entry["date"], self.datetime_format())
            >= time_24_hours_ago
        ]
        return len(movements) < 3

    def valid_amount(self):
        return (
            self.monto <= self.user["sueldo"] / 2
            and self.monto <= self.account["saldo"]
            and self.monto <= self.e.saldo_cajero
        )
