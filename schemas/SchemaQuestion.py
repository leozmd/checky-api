from pydantic import BaseModel


class Question(BaseModel):
    txtPregunta: str
    idMiembro: int
