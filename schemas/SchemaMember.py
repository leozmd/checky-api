from pydantic import BaseModel


class Member(BaseModel):
    idUsuario: int
    idClase: int
