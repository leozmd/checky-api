from pydantic import BaseModel


class Status(BaseModel):
    tipoEstado: str
    resEstado: int
