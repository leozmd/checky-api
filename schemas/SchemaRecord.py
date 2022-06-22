from datetime import date, time
from pydantic import BaseModel


class Record(BaseModel):
    diaRegistro: date
    horaRegistro: time
    idMiembro: int
    idLista: int
