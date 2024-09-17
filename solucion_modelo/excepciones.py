class ParametrosInvalidos(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Parámetros inválidos", *args)
