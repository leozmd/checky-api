from pydantic import BaseModel


class Shift(BaseModel):
    nomTurno: str
