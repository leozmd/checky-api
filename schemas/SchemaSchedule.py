from datetime import time
from pydantic import BaseModel


class Schedule(BaseModel):
    diaHorario: str
    iniHorario: time
    finHorario: time
