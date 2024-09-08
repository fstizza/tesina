from typing import Optional
from datetime import datetime

class Usuario:
    def __init__(self, dni, clave, nombre, sueldo, admin, cuenta) -> None:
        self.dni = dni 
        self.clave = clave
        self.cuenta = cuenta
        self.nombre = nombre
        self.sueldo = sueldo
        self.cuenta = cuenta
        self.admin = admin 

    def es_admin(self)-> bool:
        return self.admin
 
    def cambiar_clave(self,clave)-> Optional[str]:
        mov = filter(lambda x: x.tipo == "CAMBIO_CLAVE",self.cuenta.movimientos)
        if len(list(mov)) > 0:
            return "Limite de cambio de clave alcanzado"

        self.clave = clave
        self.cuenta._agregarMovimiento(0,"CAMBIO_CLAVE")

    def to_dict(self):
        return { 
            "dni": self.dni,
            "nombre": self.nombre,
            "clave": self.clave,
            "sueldo": self.sueldo,
            "admin": self.admin,
            "cuenta": self.cuenta.to_dict() 
        }
    @classmethod
    def from_json(cls,data):
        cuenta = Cuenta.from_json(data["cuenta"]) 
        return cls(
            data["dni"],
            data["clave"],
            data["nombre"],
            data["sueldo"],
            data["admin"],
            cuenta
        )


class Cuenta:
    def __init__(self,saldo, movimientos) -> None:
        self.saldo = saldo 
        self.movimientos = movimientos
    
    def to_dict(self):
        return { 
            "saldo": self.saldo,
            "movimientos": [ mov.to_dict() for mov in self.movimientos]
        }

    @classmethod
    def from_json(cls,data):
        movimientos = [Movimiento.from_json(data_mov) for data_mov in data["movimientos"]]
        return cls(
            data["saldo"],
            movimientos 
        )

    def debito(self,monto) -> Optional[str]:
        if self.saldo - monto < 0:
            return "Monto de la cuenta insuficiente"

        self._agregarMovimiento(monto,"DEBITO")
        self.saldo -= monto

    def credito(self,monto):
        self._agregarMovimiento(monto,"CREDITO")
        self.saldo += monto

    def _agregarMovimiento(self,monto, tipo):
        mov = Movimiento(monto,tipo,datetime.now())
        self.movimientos.append(mov)

class Movimiento:
    def __init__(self,monto,tipo,fecha) -> None:
        self.monto = monto
        self.tipo = tipo
        self.fecha = fecha

    def to_dict(self):
        return { 
            "monto": self.monto,
            "tipo": self.tipo,
            "fecha": self.fecha.isoformat()
        }

    @classmethod
    def from_json(cls,data):
        fecha = datetime.fromisoformat(data["fecha"])
        return cls(
            data["monto"],
            data["tipo"],
            fecha
        )

