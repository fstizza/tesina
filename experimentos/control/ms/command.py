from estado import Estado


class Invoker:
    def __init__(self, op_class, args):
        self.op_class = op_class
        self.args = args

    def execute_command(self):
        e = Estado.cargar()
        op = self.op_class(e, self.args)
        op.execute()
        e.guardar()
