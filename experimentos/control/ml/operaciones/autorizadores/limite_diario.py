from datetime import datetime

class LimiteDiario:
    def __init__(self,user_repo,auth) -> None:
        self.auth = auth
        self.user_repo = user_repo

    def autorizar(self, usuario, monto):
        desde = datetime.now().replace(hour=0, minute=0, second=0)
        hasta = datetime.now().replace(hour=23, minute=59, second=59)
        movs = self.user_repo.movimientosPorRango(usuario,desde,hasta)
        if len(movs)> 3:
            return "Limite diario de operaciones alcanzado"

        return self.auth.autorizar(usuario, monto)

