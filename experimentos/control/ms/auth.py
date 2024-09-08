class Auth:
    def execute(self, e, dni, clave):
        pass


class AuthAdmin(Auth):
    def execute(self, e, dni, clave):
        return dni == e.admin_user and clave == e.admin_pass


class AuthUser(Auth):
    def execute(self, e, dni, clave):
        user_list = e.user_list
        user = next((item for item in user_list if item["dni"] == dni), None)
        if user == None:
            return (None, None)
        account_list = e.account_list
        account = next(
            (
                item
                for item in account_list
                if item["dni"] == dni and item["clave"] == clave
            ),
            None,
        )

        return (user, account)
