from pydantic import BaseModel


class Answer(BaseModel):
    txtRespuesta: str
    edoRespuesta: str
    idPregunta: int
