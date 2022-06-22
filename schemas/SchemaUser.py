from pydantic import BaseModel


class User(BaseModel):
    nomUsuario: str
    appatUsuario: str
    apmatUsuario: str
    sexoUsuario: str
    matUsuario: str
    usuUsuario: str
    passUsuario: str
    idRol: int
    idEstado: int
