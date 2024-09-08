import sys

class ArgSanitizador:
    def __init__(self, args):
        """
        :param args: List of command-line arguments.
                """
        self.args = args

    def sanitizar(self,req):
        """
            Valida argumentos basado en un conjunto de parametros. 
            :param param_requirements: List of tuples where each tuple has:
                - param_name: String, name of the parameter.
                - param_type: Type (int, str, etc.) of the parameter.
                - validation_func: Function that takes the parameter and returns a boolean indicating validity.
        """
        arg_sanitizados = {}

        if len(self.args) != len(req):
            raise ValueError("Cantidad invalida de argumentos")

        for arg, (nombre, tipo, func_validacion) in zip(self.args, req):
            try:
                argumento = tipo(arg)
            except ValueError:
                raise ValueError(f"{arg} no puede ser de tipo {tipo.__name__}")
            
            # Custom validation
            if not func_validacion(argumento):
                raise ValueError(f"{arg} no puede ser validada {nombre}")

            arg_sanitizados[nombre] = argumento
        
        return arg_sanitizados
