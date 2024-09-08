from datetime import datetime


def hoy():
    ahora = datetime.now()
    return datetime(ahora.year, ahora.month, ahora.day)
