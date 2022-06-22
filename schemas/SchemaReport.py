from pydantic import BaseModel


class Report(BaseModel):
    txtReporte: str
    edoReporte: str
    resReporte: str
    idUsuario: int
