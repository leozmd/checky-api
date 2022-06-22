from pydantic import BaseModel


class Grade(BaseModel):
    tipoGrado: str
