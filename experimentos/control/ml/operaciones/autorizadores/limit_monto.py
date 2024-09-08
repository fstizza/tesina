class LimiteMonto:
    def __init__(self,user_repo,auth) -> None:
        self.auth = auth
        self.user_repo = user_repo

    def autorizar(self, usuario, monto):
        if monto > usuario.sueldo / 2:
            return "Limite de monto alcanzado"

        return self.auth.autorizar(usuario,monto)

