from abst_types import FECHAHORA
from enums import OPERACION

MOVIMIENTO = tuple[FECHAHORA, OPERACION]
#chequear de que estos ints sean naturales cuando los uso en variables, es decir > 0
MONTO = int
