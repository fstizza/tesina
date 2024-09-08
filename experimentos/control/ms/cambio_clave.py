from operacion import OperacionUser
from datetime import datetime, timedelta


class CambioClave(OperacionUser):
    def __init__(self, e, args):
        super().__init__(e, args)
        self.nueva = args[3]

    def execute(self):
        super().execute()
        if self.valid() == False:
            raise Exception("Cambio de clave no permitido")

        self.account["clave"] = self.nueva
        self.e.mov_list.append(
            {
                "mov_type": "cambio_clave",
                "dni": self.dni,
                "date": datetime.now().strftime(self.datetime_format()),
            }
        )
        return

    def valid(self):
        return self.valid_key_constraints() and self.valid_key_lifetime()

    def valid_key_constraints(self):
        return self.nueva.isalnum() and len(self.nueva) >= 8

    def valid_key_lifetime(self):
        current_time = datetime.now()
        time_a_month_ago = current_time - timedelta(days=30)

        movements = [
            entry
            for entry in self.e.mov_list
            if entry["mov_type"] == "cambio_clave"
            and entry["dni"] == self.dni
            and datetime.strptime(entry["date"], self.datetime_format())
            >= time_a_month_ago
        ]
        return len(movements) == 0
