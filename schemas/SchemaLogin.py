from pydantic import BaseModel


class Login(BaseModel):
    usuUsuario: str
    passUsuario: str
