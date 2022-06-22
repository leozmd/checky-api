from pydantic import BaseModel


class Role(BaseModel):
    tipoRol: str
