from datetime import datetime
from enums import Op

def op_to_str (op):
    if (op == Op.EXTRACCION):
        return "extraccion"
    else:
        return "clave"

def str_to_op (op):
    if (op == "extraccion"):
        return Op.EXTRACCION
    elif (op == "clave"):
        return Op.CLAVE
    else:
        print("operacion desconocida")
        exit(1)

def mov_to_str (mov):
    return [(datetime.strftime(fecha, '%Y-%m-%d %H:%M:%S'), op_to_str(op)) for (fecha, op) in mov]

def mov_to_str2 (mov):
    movs = [(datetime.strftime(fecha, '%Y-%m-%d %H:%M:%S'), op_to_str(op)) for (fecha, op) in mov]
    return ";".join(map(lambda m: str(m), movs))

def movs_to_str (movs):
    for dni,mov in movs.items():
        movs[dni] = mov_to_str(mov)
    return movs

def mov_from_str (mov):
    return [(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S'), str_to_op(op)) for (fecha, op) in mov]

def movs_from_str (movs):
    for dni,mov in movs.items():
        movs[dni] = mov_from_str(mov)
    return movs