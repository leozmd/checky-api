from datetime import datetime
from pydantic import BaseModel


class List(BaseModel):
    diaLista: datetime
    idClase: int
